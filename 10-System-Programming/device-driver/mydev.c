// Simple Character Device Driver - Educational Project
// Safe virtual device - NO hardware manipulation
#include <linux/module.h>
#include <linux/version.h>
#include <linux/kernel.h>
#include <linux/types.h>
#include <linux/kdev_t.h>
#include <linux/fs.h>
#include <linux/device.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>
#include <linux/ioctl.h>

#define DEVICE_NAME "mydev"
#define CLASS_NAME "mydev_class"
#define BUF_LEN 1024
#define PROC_NAME "mydev_stats"

// IOCTL commands
#define MYDEV_IOCTL_MAGIC 'M'
#define MYDEV_IOCTL_RESET _IO(MYDEV_IOCTL_MAGIC, 1)
#define MYDEV_IOCTL_GET_SIZE _IOR(MYDEV_IOCTL_MAGIC, 2, int)
#define MYDEV_IOCTL_CLEAR _IO(MYDEV_IOCTL_MAGIC, 3)

// Device structure
struct mydev_device {
    dev_t dev;
    struct cdev cdev;
    struct class *class;
    struct device *device;
    char buffer[BUF_LEN];
    size_t data_size;
    size_t read_pos;
    struct mutex lock;
    unsigned long open_count;
    unsigned long read_count;
    unsigned long write_count;
};

static struct mydev_device mydev;
static struct proc_dir_entry *proc_entry;

// Forward declarations
static int mydev_open(struct inode *, struct file *);
static int mydev_release(struct inode *, struct file *);
static ssize_t mydev_read(struct file *, char __user *, size_t, loff_t *);
static ssize_t mydev_write(struct file *, const char __user *, size_t, loff_t *);
static long mydev_ioctl(struct file *, unsigned int, unsigned long);

// File operations
static struct file_operations mydev_fops = {
    .owner = THIS_MODULE,
    .open = mydev_open,
    .release = mydev_release,
    .read = mydev_read,
    .write = mydev_write,
    .unlocked_ioctl = mydev_ioctl,
    .llseek = no_llseek,
};

// /proc file operations
static int proc_show(struct seq_file *m, void *v)
{
    struct mydev_device *dev = &mydev;

    seq_printf(m, "=== MyDev Statistics ===\n");
    seq_printf(m, "Device name: %s\n", DEVICE_NAME);
    seq_printf(m, "Major number: %d\n", MAJOR(dev->dev));
    seq_printf(m, "Minor number: %d\n", MINOR(dev->dev));
    seq_printf(m, "Open count: %lu\n", dev->open_count);
    seq_printf(m, "Read count: %lu\n", dev->read_count);
    seq_printf(m, "Write count: %lu\n", dev->write_count);
    seq_printf(m, "Buffer size: %zu bytes\n", BUF_LEN);
    seq_printf(m, "Data in buffer: %zu bytes\n", dev->data_size);
    seq_printf(m, "Read position: %zu\n", dev->read_pos);

    return 0;
}

static int proc_open(struct inode *inode, struct file *file)
{
    return single_open(file, proc_show, NULL);
}

static const struct proc_ops proc_fops = {
    .proc_open = proc_open,
    .proc_read = seq_read,
    .proc_lseek = seq_lseek,
    .proc_release = single_release,
};

// Open device
static int mydev_open(struct inode *inode, struct file *file)
{
    struct mydev_device *dev;

    pr_info("%s: Device opened\n", DEVICE_NAME);

    dev = container_of(inode->i_cdev, struct mydev_device, cdev);
    file->private_data = dev;

    mutex_lock(&dev->lock);
    dev->open_count++;
    mutex_unlock(&dev->lock);

    return 0;
}

// Release device
static int mydev_release(struct inode *inode, struct file *file)
{
    struct mydev_device *dev = file->private_data;

    pr_info("%s: Device closed\n", DEVICE_NAME);

    mutex_lock(&dev->lock);
    dev->open_count--;
    mutex_unlock(&dev->lock);

    return 0;
}

// Read from device
static ssize_t mydev_read(struct file *file, char __user *buf, size_t count,
                         loff_t *ppos)
{
    struct mydev_device *dev = file->private_data;
    ssize_t bytes_to_read;
    int ret = 0;

    pr_info("%s: Read requested (count=%zu)\n", DEVICE_NAME, count);

    mutex_lock(&dev->lock);

    if (dev->data_size == 0) {
        pr_info("%s: No data available\n", DEVICE_NAME);
        ret = 0; // EOF
        goto out;
    }

    // Calculate bytes to read
    bytes_to_read = dev->data_size - dev->read_pos;
    if (bytes_to_read > count)
        bytes_to_read = count;

    // Copy data to user space
    if (copy_to_user(buf, dev->buffer + dev->read_pos, bytes_to_read)) {
        pr_err("%s: copy_to_user failed\n", DEVICE_NAME);
        ret = -EFAULT;
        goto out;
    }

    dev->read_pos += bytes_to_read;
    dev->read_count++;
    ret = bytes_to_read;

    pr_info("%s: Read %zd bytes\n", DEVICE_NAME, bytes_to_read);

out:
    mutex_unlock(&dev->lock);
    return ret;
}

// Write to device
static ssize_t mydev_write(struct file *file, const char __user *buf,
                          size_t count, loff_t *ppos)
{
    struct mydev_device *dev = file->private_data;
    ssize_t bytes_to_write;

    pr_info("%s: Write requested (count=%zu)\n", DEVICE_NAME, count);

    mutex_lock(&dev->lock);

    // Reset buffer for new write
    dev->data_size = 0;
    dev->read_pos = 0;

    // Limit write size
    bytes_to_write = count;
    if (bytes_to_write > BUF_LEN)
        bytes_to_write = BUF_LEN;

    // Copy data from user space
    if (copy_from_user(dev->buffer, buf, bytes_to_write)) {
        pr_err("%s: copy_from_user failed\n", DEVICE_NAME);
        mutex_unlock(&dev->lock);
        return -EFAULT;
    }

    dev->data_size = bytes_to_write;
    dev->write_count++;

    pr_info("%s: Wrote %zd bytes\n", DEVICE_NAME, bytes_to_write);

    mutex_unlock(&dev->lock);
    return bytes_to_write;
}

// IOCTL commands
static long mydev_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
    struct mydev_device *dev = file->private_data;
    int ret = 0;
    int size;

    pr_info("%s: IOCTL called (cmd=%u)\n", DEVICE_NAME, cmd);

    mutex_lock(&dev->lock);

    switch (cmd) {
    case MYDEV_IOCTL_RESET:
        // Reset read position to beginning
        dev->read_pos = 0;
        pr_info("%s: Buffer reset\n", DEVICE_NAME);
        break;

    case MYDEV_IOCTL_GET_SIZE:
        // Return data size
        size = dev->data_size;
        if (copy_to_user((int __user *)arg, &size, sizeof(int))) {
            ret = -EFAULT;
            pr_err("%s: IOCTL copy_to_user failed\n", DEVICE_NAME);
        }
        pr_info("%s: Data size: %d\n", DEVICE_NAME, size);
        break;

    case MYDEV_IOCTL_CLEAR:
        // Clear buffer
        dev->data_size = 0;
        dev->read_pos = 0;
        memset(dev->buffer, 0, BUF_LEN);
        pr_info("%s: Buffer cleared\n", DEVICE_NAME);
        break;

    default:
        pr_warn("%s: Unknown IOCTL command: %u\n", DEVICE_NAME, cmd);
        ret = -ENOTTY;
        break;
    }

    mutex_unlock(&dev->lock);
    return ret;
}

// Module initialization
static int __init mydev_init(void)
{
    int ret;

    pr_info("%s: Initializing module\n", DEVICE_NAME);

    // Initialize device structure
    memset(&mydev, 0, sizeof(mydev));
    mutex_init(&mydev.lock);

    // Allocate major and minor numbers dynamically
    ret = alloc_chrdev_region(&mydev.dev, 0, 1, DEVICE_NAME);
    if (ret < 0) {
        pr_err("%s: Failed to allocate chrdev region\n", DEVICE_NAME);
        return ret;
    }

    pr_info("%s: Allocated major=%d minor=%d\n", DEVICE_NAME,
            MAJOR(mydev.dev), MINOR(mydev.dev));

    // Initialize cdev
    cdev_init(&mydev.cdev, &mydev_fops);
    mydev.cdev.owner = THIS_MODULE;

    // Add cdev to kernel
    ret = cdev_add(&mydev.cdev, mydev.dev, 1);
    if (ret < 0) {
        pr_err("%s: Failed to add cdev\n", DEVICE_NAME);
        goto error_cdev;
    }

    // Create device class
    mydev.class = class_create(CLASS_NAME);
    if (IS_ERR(mydev.class)) {
        pr_err("%s: Failed to create class\n", DEVICE_NAME);
        ret = PTR_ERR(mydev.class);
        goto error_class;
    }

    // Create device
    mydev.device = device_create(mydev.class, NULL, mydev.dev, NULL, DEVICE_NAME);
    if (IS_ERR(mydev.device)) {
        pr_err("%s: Failed to create device\n", DEVICE_NAME);
        ret = PTR_ERR(mydev.device);
        goto error_device;
    }

    // Create /proc entry
    proc_entry = proc_create(PROC_NAME, 0666, NULL, &proc_fops);
    if (!proc_entry) {
        pr_err("%s: Failed to create /proc entry\n", DEVICE_NAME);
        ret = -ENOMEM;
        goto error_proc;
    }

    pr_info("%s: Module loaded successfully\n", DEVICE_NAME);
    pr_info("%s: Device file: /dev/%s\n", DEVICE_NAME, DEVICE_NAME);
    pr_info("%s: Proc entry: /proc/%s\n", DEVICE_NAME, PROC_NAME);

    return 0;

error_proc:
    device_destroy(mydev.class, mydev.dev);
error_device:
    class_destroy(mydev.class);
error_class:
    cdev_del(&mydev.cdev);
error_cdev:
    unregister_chrdev_region(mydev.dev, 1);
    return ret;
}

// Module cleanup
static void __exit mydev_exit(void)
{
    pr_info("%s: Unloading module\n", DEVICE_NAME);

    // Remove /proc entry
    if (proc_entry)
        remove_proc_entry(PROC_NAME, NULL);

    // Destroy device
    device_destroy(mydev.class, mydev.dev);

    // Destroy class
    class_destroy(mydev.class);

    // Remove cdev
    cdev_del(&mydev.cdev);

    // Unregister character device
    unregister_chrdev_region(mydev.dev, 1);

    pr_info("%s: Module unloaded successfully\n", DEVICE_NAME);
}

module_init(mydev_init);
module_exit(mydev_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Educational Project");
MODULE_DESCRIPTION("Simple character device driver for learning");
MODULE_VERSION("1.0");
