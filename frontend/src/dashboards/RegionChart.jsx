import React from "react";
import ReactECharts from "echarts-for-react";
import { setFilter } from "../state/filtersStore";

export default function RegionChart({ decisions }) {
  if (!decisions || decisions.length === 0) {
    return <p>No data available.</p>;
  }

  const counts = {};
  decisions.forEach((d) => {
    const r = d.region || "UNKNOWN";
    counts[r] = (counts[r] || 0) + 1;
  });

  const regions = Object.keys(counts);
  const values = Object.values(counts);

  const option = {
    title: {
      text: "Region Distribution",
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
      bottom: 80,
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: regions,
      axisLabel: { rotate: 30 },
      name: "Region",
      nameLocation: "middle",
      nameGap: 60,
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
      setFilter("region", params.name);
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