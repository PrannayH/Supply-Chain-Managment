import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Products = () => {
  const [productData, setProductData] = useState([]);

  useEffect(() => {
    // Fetch data from the /predict endpoint
    axios.get('http://127.0.0.1:5000/predict')
      .then(response => {
        // Extract product data from the response
        const products = response.data.demand;
        setProductData(products);

        // Debug: Log the received data
        console.log('Received product data:', products);
      })
      .catch(error => {
        console.error('Error fetching product data:', error);
      });
  }, []);

  return (
    <div className='ml-10 flex justify-center items-center'>
  <div className='text-center'>
    <h2 className='text-blue-400 font-mono font-bold text-2xl mb-8'>Top 8 In-Demand Products</h2>
    <table>
      <thead>
        <tr className='bg-blue-500'>
          <th className='px-3 py-3 text-white'>Drug name</th>
          <th className='px-3 py-3 text-white'>Forecasted Demand (Qty.)</th>
        </tr>
      </thead>
      <tbody>
        {productData.map((product, index) => (
          <tr key={product['Product ID']} className={index % 2 === 0 ? 'bg-gray-300' : 'bg-gray-400'}>
            <td className='px-6 py-2'>{product['Product ID']}</td>
            <td className='px-10 py-2'>{product['Forecasted Demand']}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
</div>

  );
}

export default Products;
