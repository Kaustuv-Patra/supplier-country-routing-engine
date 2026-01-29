import React from "react";
import ReactECharts from "echarts-for-react";

/**
 * RoutingCodeChart
 *
 * Displays distribution of routing codes (e.g. APAC-SEA).
 * Axis layout is explicitly tuned to avoid label overlap.
 */
export default function RoutingCodeChart({ decisions }) {
  if (!decisions || decisions.length === 0) {
    return <p>No data available for routing code distribution.</p>;
  }

  const routingCounts = {};

  decisions.forEach((d) => {
    const code = d.routing_code || "UNKNOWN";
    routingCounts[code] = (routingCounts[code] || 0) + 1;
  });

  const codes = Object.keys(routingCounts);
  const counts = Object.values(routingCounts);

  const option = {
    title: {
      text: "Routing Code Breakdown",
      left: "center",
      top: 10,
    },
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "shadow" },
      formatter: "{b}: {c} invoices",
    },
    grid: {
      top: 70,
      left: "12%",
      right: "8%",
      bottom: 120, // ⬅ extra space for rotated labels + axis name
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: codes,
      axisLabel: {
        rotate: 45,
        interval: 0,
      },
      name: "Routing Code",
      nameLocation: "middle",
      nameGap: 90, // ⬅ pushes name below labels
    },
    yAxis: {
      type: "value",
      name: "Invoices",
    },
    series: [
      {
        type: "bar",
        data: counts,
        emphasis: { focus: "series" },
      },
    ],
  };

  return (
    <ReactECharts
      option={option}
      style={{ height: "400px", width: "100%" }}
    />
  );
}