import React from "react";
import ReactECharts from "echarts-for-react";

/**
 * CountryChart
 *
 * Displays supplier country distribution using Apache ECharts.
 */
export default function CountryChart({ decisions }) {
  if (!decisions || decisions.length === 0) {
    return <p>No data available for country distribution.</p>;
  }

  const countryCounts = {};

  decisions.forEach((decision) => {
    const country = decision.predicted_country || "Unknown";
    countryCounts[country] = (countryCounts[country] || 0) + 1;
  });

  const countries = Object.keys(countryCounts);
  const counts = Object.values(countryCounts);

  const option = {
    title: {
      text: "Supplier Country Distribution",
      left: "center",
    },
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "shadow" },
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "10%",
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: countries,
      axisLabel: {
        rotate: 45,
        interval: 0,
      },
    },
    yAxis: {
      type: "value",
      name: "Invoices",
    },
    series: [
      {
        name: "Invoices",
        type: "bar",
        data: counts,
        emphasis: {
          focus: "series",
        },
      },
    ],
  };

  return <ReactECharts option={option} style={{ height: "400px", width: "100%" }} />;
}