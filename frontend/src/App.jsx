import React from 'react' 
import { BrowserRouter, Link, Route, Routes} from 'react-router-dom';  

import { supplierImg } from './assets';
import { Home, Products, Track } from './pages';

const App = () => {
  return (
    <BrowserRouter>
      <header className='w-full bg-black flex justify-between items-center sm:px-8 px-4 py-4'>
        <Link to="/home" className="flex items-center">
          <img src={supplierImg} className="w-14 h-14 rounded-full flex" alt="" />
            <span className='ml-2 text-cyan-200 font-mono font-bold text-xl'>SmartSuppliers</span>
        </Link>
        <span>
          <Link to="/home" className='font-mono font-bold text-lg bg-green-300 text-black px-4 py-2 rounded-md'>Home</Link>
          &nbsp; 
          &nbsp;
          <Link to="/products" className="font-mono font-bold text-lg bg-green-300 text-black px-4 py-2 rounded-md">Products</Link>
          &nbsp;
          &nbsp;
          <Link to="/track" className="font-mono font-bold text-lg bg-green-300 text-black px-4 py-2 rounded-md">Track</Link>
         </span>
        
      </header>
      {/* <ToastContainer position="bottom-right" /> */}

      <main className="sm:p-8 bg-black px-4 py-8 w-full min-h-[calc(100vh-73px)]">
        <Routes>
          <Route path="/home" element={<Home />} />
          <Route path="/products" element={<Products />} />
          <Route path="/track" element={<Track/>} />
        </Routes>
      </main> 
      
    </BrowserRouter>
  )
}

export default App