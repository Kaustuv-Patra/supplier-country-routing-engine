import React from "react";
import ReactECharts from "echarts-for-react";
import { setFilter } from "../state/filtersStore";

export default function ConfidenceSplitChart({ decisions }) {
  if (!decisions || decisions.length === 0) {
    return <p>No data available.</p>;
  }

  let low = 0;
  let medium = 0;
  let high = 0;

  decisions.forEach((d) => {
    const c = d.confidence ?? 0;
    if (c < 0.08) low++;
    else if (c <= 0.1) medium++;
    else high++;
  });

  const option = {
    title: {
      text: "Confidence Level Split",
      left: "center",
      top: 10,
    },
    tooltip: {
      trigger: "item",
      formatter: "{b}: {c} invoices ({d}%)",
    },
    legend: {
      bottom: 10,
    },
    series: [
      {
        type: "pie",
        radius: ["40%", "70%"],
        data: [
          { value: low, name: "Low (< 0.08)" },
          { value: medium, name: "Medium (0.08–0.10)" },
          { value: high, name: "High (> 0.10)" },
        ],
        label: {
          formatter: "{b}\n{d}%",
        },
      },
    ],
  };

  const onEvents = {
    click: (params) => {
      if (params.name.startsWith("Low")) {
        setFilter("confidence_band", "low");
      } else if (params.name.startsWith("Medium")) {
        setFilter("confidence_band", "medium");
      } else if (params.name.startsWith("High")) {
        setFilter("confidence_band", "high");
      }
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