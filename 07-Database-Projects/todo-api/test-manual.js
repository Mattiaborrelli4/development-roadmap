/**
 * Script di Test Manuale per TODO API
 * Esegui con: node test-manual.js
 *
 * Richiede: node installato e API server in esecuzione
 */

const http = require('http');

const BASE_URL = 'http://localhost:3000';

// Colori per console
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[36m',
  magenta: '\x1b[35m'
};

function makeRequest(method, path, data = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, BASE_URL);
    const options = {
      hostname: url.hostname,
      port: url.port || 3000,
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(body);
          resolve({ status: res.statusCode, data: parsed });
        } catch (e) {
          resolve({ status: res.statusCode, data: body });
        }
      });
    });

    req.on('error', reject);

    if (data) {
      req.write(JSON.stringify(data));
    }

    req.end();
  });
}

async function runTests() {
  console.log(`${colors.magenta}=====================================${colors.reset}`);
  console.log(`${colors.magenta}TODO API - Test Suite${colors.reset}`);
  console.log(`${colors.magenta}=====================================${colors.reset}\n`);

  let testId = null;

  // Test 1: Root endpoint
  console.log(`${colors.blue}Test 1: GET /${colors.reset}`);
  try {
    const result = await makeRequest('GET', '/');
    console.log(`Status: ${colors.green}${result.status}${colors.reset}`);
    console.log('Response:', JSON.stringify(result.data, null, 2));
  } catch (error) {
    console.log(`${colors.red}Error: ${error.message}${colors.reset}`);
  }
  console.log('');

  // Test 2: Create todo
  console.log(`${colors.blue}Test 2: POST /api/todos${colors.reset}`);
  try {
    const newTodo = {
      title: 'Comprare latte',
      description: 'Andare al supermercato',
      completed: false
    };
    const result = await makeRequest('POST', '/api/todos', newTodo);
    console.log(`Status: ${colors.green}${result.status}${colors.reset}`);
    console.log('Response:', JSON.stringify(result.data, null, 2));
    testId = result.data.data.id;
  } catch (error) {
    console.log(`${colors.red}Error: ${error.message}${colors.reset}`);
  }
  console.log('');

  // Test 3: Get all todos
  console.log(`${colors.blue}Test 3: GET /api/todos${colors.reset}`);
  try {
    const result = await makeRequest('GET', '/api/todos');
    console.log(`Status: ${colors.green}${result.status}${colors.reset}`);
    console.log('Response:', JSON.stringify(result.data, null, 2));
  } catch (error) {
    console.log(`${colors.red}Error: ${error.message}${colors.reset}`);
  }
  console.log('');

  // Test 4: Get specific todo
  if (testId) {
    console.log(`${colors.blue}Test 4: GET /api/todos/${testId}${colors.reset}`);
    try {
      const result = await makeRequest('GET', `/api/todos/${testId}`);
      console.log(`Status: ${colors.green}${result.status}${colors.reset}`);
      console.log('Response:', JSON.stringify(result.data, null, 2));
    } catch (error) {
      console.log(`${colors.red}Error: ${error.message}${colors.reset}`);
    }
    console.log('');
  }

  // Test 5: Update todo
  if (testId) {
    console.log(`${colors.blue}Test 5: PUT /api/todos/${testId}${colors.reset}`);
    try {
      const updateData = {
        title: 'Comprare latte e pane',
        completed: true
      };
      const result = await makeRequest('PUT', `/api/todos/${testId}`, updateData);
      console.log(`Status: ${colors.green}${result.status}${colors.reset}`);
      console.log('Response:', JSON.stringify(result.data, null, 2));
    } catch (error) {
      console.log(`${colors.red}Error: ${error.message}${colors.reset}`);
    }
    console.log('');
  }

  // Test 6: Toggle todo
  if (testId) {
    console.log(`${colors.blue}Test 6: PATCH /api/todos/${testId}/toggle${colors.reset}`);
    try {
      const result = await makeRequest('PATCH', `/api/todos/${testId}/toggle`);
      console.log(`Status: ${colors.green}${result.status}${colors.reset}`);
      console.log('Response:', JSON.stringify(result.data, null, 2));
    } catch (error) {
      console.log(`${colors.red}Error: ${error.message}${colors.reset}`);
    }
    console.log('');
  }

  // Test 7: Delete todo
  if (testId) {
    console.log(`${colors.blue}Test 7: DELETE /api/todos/${testId}${colors.reset}`);
    try {
      const result = await makeRequest('DELETE', `/api/todos/${testId}`);
      console.log(`Status: ${colors.green}${result.status}${colors.reset}`);
      console.log('Response:', JSON.stringify(result.data, null, 2));
    } catch (error) {
      console.log(`${colors.red}Error: ${error.message}${colors.reset}`);
    }
    console.log('');
  }

  // Test 8: Validation error
  console.log(`${colors.blue}Test 8: POST /api/todos (validation test)${colors.reset}`);
  try {
    const invalidTodo = { title: '' };
    const result = await makeRequest('POST', '/api/todos', invalidTodo);
    console.log(`Status: ${colors.yellow}${result.status}${colors.reset}`);
    console.log('Response:', JSON.stringify(result.data, null, 2));
  } catch (error) {
    console.log(`${colors.red}Error: ${error.message}${colors.reset}`);
  }
  console.log('');

  // Test 9: 404 error
  console.log(`${colors.blue}Test 9: GET /api/todos/99999 (404 test)${colors.reset}`);
  try {
    const result = await makeRequest('GET', '/api/todos/99999');
    console.log(`Status: ${colors.yellow}${result.status}${colors.reset}`);
    console.log('Response:', JSON.stringify(result.data, null, 2));
  } catch (error) {
    console.log(`${colors.red}Error: ${error.message}${colors.reset}`);
  }
  console.log('');

  console.log(`${colors.magenta}=====================================${colors.reset}`);
  console.log(`${colors.green}Test Suite Completata!${colors.reset}`);
  console.log(`${colors.magenta}=====================================${colors.reset}`);
}

// Esegui i test
runTests().catch(console.error);
