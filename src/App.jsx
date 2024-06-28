

import './App.css'
import React, {useState} from 'react';
import FirstPage from "./routes/FirstPage"
import {Route,Routes} from "react-router-dom"
import Acceuil from './routes/Acceuil'
import Resrech from './routes/Resrech';
import Profil from './routes/Profil';
import MesAnnonces from './routes/MesAnnonces';

function App() {
 

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Acceuil/>}/>
        <Route path="/resrech" element={<Resrech/>}/>
        <Route path="/profil" element={<Profil/>}/>
        <Route path="/mesan" element={<MesAnnonces/>}/>
      </Routes>
      
    </div>
  )
}
export default App

