import React from "react";
import ReactECharts from "echarts-for-react";

/**
 * RegionChart
 *
 * Displays region / continent distribution (APAC / EMEA / AMER).
 */
export default function RegionChart({ decisions }) {
  if (!decisions || decisions.length === 0) {
    return <p>No data available for region distribution.</p>;
  }

  const regionCounts = {
    APAC: 0,
    EMEA: 0,
    AMER: 0,
  };

  decisions.forEach((decision) => {
    const region = decision.region;
    if (regionCounts[region] !== undefined) {
      regionCounts[region] += 1;
    }
  });

  const data = Object.entries(regionCounts)
    .filter(([, count]) => count > 0)
    .map(([region, count]) => ({
      name: region,
      value: count,
    }));

  const option = {
    title: {
      text: "Region / Continent Distribution",
      left: "center",
    },
    tooltip: {
      trigger: "item",
      formatter: "{b}: {c} invoices ({d}%)",
    },
    legend: {
      orient: "horizontal",
      bottom: 0,
    },
    series: [
      {
        name: "Invoices",
        type: "pie",
        radius: ["40%", "70%"],
        data,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: "rgba(0, 0, 0, 0.4)",
          },
        },
      },
    ],
  };

  return <ReactECharts option={option} style={{ height: "400px", width: "100%" }} />;
}