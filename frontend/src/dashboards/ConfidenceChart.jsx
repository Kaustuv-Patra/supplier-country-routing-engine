import React from "react";
import ReactECharts from "echarts-for-react";

/**
 * ConfidenceChart
 *
 * Fine-grained histogram of model confidence scores.
 * Tailored for low-confidence multi-class models.
 */
export default function ConfidenceChart({ decisions }) {
  if (!decisions || decisions.length === 0) {
    return <p>No data available for confidence distribution.</p>;
  }

  // Fine-grained buckets (realistic for this model)
  const buckets = {
    "0.00–0.05": 0,
    "0.05–0.07": 0,
    "0.07–0.09": 0,
    "0.09–0.11": 0,
    "0.11–0.13": 0,
    "0.13–0.15": 0,
    "0.15+": 0,
  };

  decisions.forEach((d) => {
    const c = d.confidence ?? 0;

    if (c < 0.05) buckets["0.00–0.05"]++;
    else if (c < 0.07) buckets["0.05–0.07"]++;
    else if (c < 0.09) buckets["0.07–0.09"]++;
    else if (c < 0.11) buckets["0.09–0.11"]++;
    else if (c < 0.13) buckets["0.11–0.13"]++;
    else if (c < 0.15) buckets["0.13–0.15"]++;
    else buckets["0.15+"]++;
  });

  const labels = Object.keys(buckets);
  const values = Object.values(buckets);

  const option = {
    title: {
      text: "Confidence Score Distribution",
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
      left: "10%",
      right: "8%",
      bottom: 70,
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: labels,
      name: "Confidence Score",
      nameLocation: "middle",
      nameGap: 40,
    },
    yAxis: {
      type: "value",
      name: "Invoices",
    },
    series: [
      {
        type: "bar",
        data: values,
        emphasis: { focus: "series" },
      },
    ],
  };

  return <ReactECharts option={option} style={{ height: "400px", width: "100%" }} />;
}