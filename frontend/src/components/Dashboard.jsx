import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { RefreshCw } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Dashboard() {
  const [data, setData] = useState([]);

  const fetchData = async () => {
    try {
      const res = await fetch('http://<IP_DU_SERVEUR>:5000/api/data');
      const json = await res.json();
      setData(json.map(d => ({
        ...d,
        time: new Date(d.timestamp * 1000).toLocaleTimeString()
      })));
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchData();
    const id = setInterval(fetchData, 5000);
    return () => clearInterval(id);
  }, []);

  // Calculate averages
  const avgTemp = data.length > 0
    ? (data.reduce((sum, d) => sum + d.temperature, 0) / data.length).toFixed(1)
    : '–';
  const avgPres = data.length > 0
    ? (data.reduce((sum, d) => sum + d.pression, 0) / data.length).toFixed(1)
    : '–';

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
      {/* Average display */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
        <div className="p-4 bg-white rounded-2xl shadow">
          <h3 className="text-lg font-medium text-gray-700">Température Moyenne</h3>
          <p className="text-4xl font-bold text-red-600 mt-2">{avgTemp}°C</p>
        </div>
        <div className="p-4 bg-white rounded-2xl shadow">
          <h3 className="text-lg font-medium text-gray-700">Pression Moyenne</h3>
          <p className="text-4xl font-bold text-blue-600 mt-2">{avgPres} Pa</p>
        </div>
      </div>

      {/* Chart header */}
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-xl font-semibold">Évolution</h2>
        <button onClick={fetchData} className="p-2 rounded-full shadow hover:bg-gray-200">
          <RefreshCw className="w-5 h-5 text-gray-700" />
        </button>
      </div>

      {/* Line Chart */}
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="temperature" stroke="#e34f26" dot={false} name="Température (°C)" />
          <Line type="monotone" dataKey="pression" stroke="#1e40af" dot={false} name="Pression (Pa)" />
        </LineChart>
      </ResponsiveContainer>
    </motion.div>
  );
}
