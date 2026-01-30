import React from "react";
import ReactECharts from "echarts-for-react";
import { setFilter } from "../state/filtersStore";

/**
 * CountryChart
 *
 * Click a country bar to filter the dashboard by country.
 */
export default function CountryChart({ decisions }) {
  if (!decisions || decisions.length === 0) {
    return <p>No data available.</p>;
  }

  const counts = {};
  decisions.forEach((d) => {
    const c = d.predicted_country || "UNKNOWN";
    counts[c] = (counts[c] || 0) + 1;
  });

  const countries = Object.keys(counts);
  const values = Object.values(counts);

  const option = {
    title: {
      text: "Supplier Country Distribution",
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
      bottom: 100,
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: countries,
      axisLabel: {
        rotate: 45,
        interval: 0,
      },
      name: "Country",
      nameLocation: "middle",
      nameGap: 70,
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

  const onEvents = {
    click: (params) => {
      setFilter("country", params.name);
      // force React re-render via store update side effect
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