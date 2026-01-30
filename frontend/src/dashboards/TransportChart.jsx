import React from "react";
import ReactECharts from "echarts-for-react";
import { setFilter } from "../state/filtersStore";

export default function TransportChart({ decisions }) {
  if (!decisions || decisions.length === 0) {
    return <p>No data available.</p>;
  }

  const counts = {};
  decisions.forEach((d) => {
    const t = d.primary_transport || "UNKNOWN";
    counts[t] = (counts[t] || 0) + 1;
  });

  const transports = Object.keys(counts);
  const values = Object.values(counts);

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
    grid: {
      top: 60,
      left: "12%",
      right: "8%",
      bottom: 80,
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: transports,
      name: "Transport Mode",
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
      setFilter("primary_transport", params.name);
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