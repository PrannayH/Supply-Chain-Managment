import React from 'react'
import { homeImg } from '../assets'

const Home = () => {
  return (
    <div className='flex'>
        <img src={homeImg} className='mt-10 ml-20 w-70 h-80 rounded-lg'/>
        <div className='flex flex-col mt-10'>
            <p className='ml-10 font-mono text-xl text-white'>The initiative is designed to create a state-of-the-art supply chain management system, anchored in transparency and enhanced demand prediction. By utilizing Ethereum, a renowned blockchain platform, the system will register suppliers as nodes to secure traceability, thus fostering trust among consumers and retailers. Advanced data analytics, powered by ARIMA models and LSTM deep learning, will be harnessed to precisely forecast product demand, ensuring supply management is both effective and efficient. Additionally, the application of inventory optimization algorithms like EOQ will ensure that inventory levels are kept at an optimum, reducing costs and boosting operational efficiency.</p>
        </div>
    </div>
  )
}

export default Home