import { useState } from 'react';
import Plot from 'react-plotly.js';
import { ChartBarIcon, TableCellsIcon } from '@heroicons/react/24/solid';

const DataVisualization = ({ chartData, tableData }) => {
  const [activeTab, setActiveTab] = useState('charts');

  const renderCharts = () => {
    if (!chartData) return null;

    return (
      <div className="space-y-6">
        {chartData.price_trends && (
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Price Trends</h3>
            <Plot
              data={chartData.price_trends.data}
              layout={{
                ...chartData.price_trends.layout,
                autosize: true,
                height: 350,
                margin: { t: 20, r: 20, b: 40, l: 60 },
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                font: {
                  family: 'Inter, system-ui, sans-serif',
                },
                xaxis: {
                  gridcolor: '#f0f0f0',
                  showgrid: true,
                },
                yaxis: {
                  gridcolor: '#f0f0f0',
                  showgrid: true,
                },
              }}
              config={{
                responsive: true,
                displayModeBar: false,
              }}
              className="w-full"
            />
          </div>
        )}

        {chartData.demand_trends && (
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Demand Trends</h3>
            <Plot
              data={chartData.demand_trends.data}
              layout={{
                ...chartData.demand_trends.layout,
                autosize: true,
                height: 350,
                margin: { t: 20, r: 20, b: 40, l: 60 },
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                font: {
                  family: 'Inter, system-ui, sans-serif',
                },
                xaxis: {
                  gridcolor: '#f0f0f0',
                  showgrid: true,
                },
                yaxis: {
                  gridcolor: '#f0f0f0',
                  showgrid: true,
                },
              }}
              config={{
                responsive: true,
                displayModeBar: false,
              }}
              className="w-full"
            />
          </div>
        )}
      </div>
    );
  };

  const renderTable = () => {
    if (!tableData || tableData.length === 0) return null;

    const headers = Object.keys(tableData[0]);

    return (
      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="data-table">
            <thead>
              <tr>
                {headers.map((header) => (
                  <th key={header} className="table-header">
                    {header.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {tableData.map((row, rowIndex) => (
                <tr
                  key={rowIndex}
                  className={rowIndex % 2 === 0 ? 'bg-white' : 'bg-gray-50'}
                >
                  {headers.map((header) => (
                    <td key={`${rowIndex}-${header}`} className="table-cell">
                      {typeof row[header] === 'number'
                        ? row[header].toLocaleString('en-IN', {
                            maximumFractionDigits: 2,
                            style: header.toLowerCase().includes('price') ? 'currency' : 'decimal',
                            currency: 'INR',
                          })
                        : row[header]}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-4">
      <div className="flex space-x-2 p-1 bg-gray-100 rounded-lg w-fit">
        <button
          className={`tab-button ${
            activeTab === 'charts' ? 'tab-button-active' : 'tab-button-inactive'
          }`}
          onClick={() => setActiveTab('charts')}
        >
          <ChartBarIcon className="w-4 h-4" />
          <span>Charts</span>
        </button>
        <button
          className={`tab-button ${
            activeTab === 'table' ? 'tab-button-active' : 'tab-button-inactive'
          }`}
          onClick={() => setActiveTab('table')}
        >
          <TableCellsIcon className="w-4 h-4" />
          <span>Table</span>
        </button>
      </div>

      <div className="transition-all duration-300 ease-in-out">
        {activeTab === 'charts' ? renderCharts() : renderTable()}
      </div>
    </div>
  );
};

export default DataVisualization; 