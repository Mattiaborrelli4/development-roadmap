import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { VictoryBar, VictoryLine, VictoryPie, VictoryChart, VictoryTheme, VictoryAxis, VictoryContainer } from 'victory-native';
import { theme } from '../styles/theme';

const ProgressChart = ({ type, data, title }) => {
  const chartData = data || [];
  const colors = theme.chartColors;

  const renderChart = () => {
    switch (type) {
      case 'bar':
        return (
          <VictoryChart
            theme={VictoryTheme.material}
            height={200}
            width={350}
            padding={{ top: 20, bottom: 40, left: 40, right: 20 }}
          >
            <VictoryBar
              data={chartData}
              x="label"
              y="value"
              style={{
                data: {
                  fill: theme.colors.primary,
                  width: 20
                }
              }}
              cornerRadius={{ top: 5 }}
              animate={{
                duration: 500,
                onLoad: { duration: 500 }
              }}
            />
            <VictoryAxis
              style={{
                tickLabels: {
                  fontSize: 10,
                  fill: theme.colors.textSecondary
                }
              }}
            />
          </VictoryChart>
        );

      case 'line':
        return (
          <VictoryChart
            theme={VictoryTheme.material}
            height={200}
            width={350}
            padding={{ top: 20, bottom: 40, left: 50, right: 20 }}
          >
            <VictoryLine
              data={chartData}
              x="label"
              y="value"
              style={{
                data: {
                  stroke: theme.colors.secondary,
                  strokeWidth: 3
                }
              }}
              animate={{
                duration: 500,
                onLoad: { duration: 500 }
              }}
            />
            <VictoryAxis
              style={{
                tickLabels: {
                  fontSize: 10,
                  fill: theme.colors.textSecondary
                }
              }}
            />
          </VictoryChart>
        );

      case 'pie':
        return (
          <View style={styles.pieContainer}>
            <VictoryPie
              data={chartData}
              x="label"
              y="value"
              colorScale={colors}
              radius={80}
              innerRadius={40}
              labels={({ datum }) => `${datum.x}\n${datum.y}`}
              style={{
                labels: {
                  fontSize: 10,
                  fill: theme.colors.surface,
                  fontWeight: 'bold'
                }
              }}
              animate={{
                duration: 500,
                onLoad: { duration: 500 }
              }}
            />
          </View>
        );

      default:
        return null;
    }
  };

  if (chartData.length === 0) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>{title}</Text>
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyText}>Nessun dato disponibile</Text>
        </View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
      <ScrollView horizontal showsHorizontalScrollIndicator={false}>
        {renderChart()}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.md,
    padding: theme.spacing.md,
    marginBottom: theme.spacing.md,
    ...theme.shadows.sm,
  },
  title: {
    fontSize: theme.fontSize.lg,
    fontWeight: '600',
    color: theme.colors.text,
    marginBottom: theme.spacing.md,
  },
  pieContainer: {
    alignItems: 'center',
    paddingVertical: theme.spacing.md,
  },
  emptyContainer: {
    paddingVertical: theme.spacing.xl,
    alignItems: 'center',
  },
  emptyText: {
    fontSize: theme.fontSize.md,
    color: theme.colors.textSecondary,
  },
});

export default ProgressChart;
