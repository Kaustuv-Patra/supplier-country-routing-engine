import React from "react";
import ReactECharts from "echarts-for-react";
import { setFilter } from "../state/filtersStore";

/**
 * RoutingCodeChart
 *
 * Clicking a routing code applies compound filters:
 *   - region
 *   - primary_transport
 */
export default function RoutingCodeChart({ decisions }) {
  if (!decisions || decisions.length === 0) {
    return <p>No data available.</p>;
  }

  const counts = {};
  decisions.forEach((d) => {
    const code = d.routing_code || "UNKNOWN";
    counts[code] = (counts[code] || 0) + 1;
  });

  const codes = Object.keys(counts);
  const values = Object.values(counts);

  const option = {
    title: {
      text: "Routing Code Breakdown",
      left: "center",
      top: 10,
    },
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "shadow" },
    },
    grid: {
      top: 60,
      left: "12%",
      right: "8%",
      bottom: 120,
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
      nameGap: 90,
    },
    yAxis: {
      type: "value",
      name: "Invoices",
    },
    series: [
      {
        type: "bar",
        data: values,
      },
    ],
  };

  const onEvents = {
    click: (params) => {
      const code = params.name;

      if (!code || !code.includes("-")) return;

      const [region, transport] = code.split("-");

      // Apply compound filters
      setFilter("region", region);
      setFilter("primary_transport", transport);

      window.dispatchEvent(new Event("filters-changed"));
    },
  };

  return (
    <ReactECharts
      option={option}
      onEvents={onEvents}
      style={{ height: "100%", width: "100%" }}
    />
  );
}