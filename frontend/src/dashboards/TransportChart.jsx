import React from "react";
import ReactECharts from "echarts-for-react";

/**
 * TransportChart
 *
 * Displays distribution of transport modes (Primary vs Secondary)
 * with proper spacing for title, legend, and bars.
 */
export default function TransportChart({ decisions }) {
  if (!decisions || decisions.length === 0) {
    return <p>No data available for transport distribution.</p>;
  }

  const primaryCounts = {};
  const secondaryCounts = {};

  decisions.forEach((decision) => {
    const primary = decision.primary_transport;
    const secondary = decision.secondary_transport;

    if (primary) {
      primaryCounts[primary] = (primaryCounts[primary] || 0) + 1;
    }

    if (secondary) {
      secondaryCounts[secondary] = (secondaryCounts[secondary] || 0) + 1;
    }
  });

  const transportModes = Array.from(
    new Set([
      ...Object.keys(primaryCounts),
      ...Object.keys(secondaryCounts),
    ])
  );

  const primaryData = transportModes.map((mode) => primaryCounts[mode] || 0);
  const secondaryData = transportModes.map((mode) => secondaryCounts[mode] || 0);

  const option = {
    title: {
      text: "Transport Mode Distribution",
      left: "center",
      top: 10,
    },
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "shadow" },
    },
    legend: {
      top: 40,
      left: "center",
      orient: "horizontal",
    },
    grid: {
      top: 90,
      left: "8%",
      right: "8%",
      bottom: "10%",
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: transportModes,
      axisLabel: {
        rotate: 0,
      },
    },
    yAxis: {
      type: "value",
      name: "Invoices",
    },
    series: [
      {
        name: "Primary Transport",
        type: "bar",
        data: primaryData,
        barGap: "20%",
        emphasis: { focus: "series" },
      },
      {
        name: "Secondary Transport",
        type: "bar",
        data: secondaryData,
        emphasis: { focus: "series" },
      },
    ],
  };

  return <ReactECharts option={option} style={{ height: "400px", width: "100%" }} />;
}