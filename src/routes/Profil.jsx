import Navbar from "../components/Navbar";
import './Profil.css';
import React, { useState } from "react";
import an from '../img/PageOne.png'
export const    Profil = () => {
const  [firstName,setFirstName]=useState('Amina');
const  [lastName,setLastName]=useState('Laggoun');
const  [pp,setPp]=useState(an);
    return (
    <>
           <Navbar/>
           <div className="main">
                <div className="photoname">
                    <h1 className="name">{firstName}</h1>
                    <h2 className="name">{lastName}</h2>
                    <img src={pp}></img>
                </div>
                <div className="info">
                       <input value={firstName} onChange={(e) => setFirstName(e.target.value)} type="text" placeholder={firstName} id="name" name="name" />
                       <input value={lastName} onChange={(e) => setLastName(e.target.value)} type="text" placeholder={lastName} id="name2" name="name2" />
                </div>
           </div>
            
             
    </>
    )
}
export default Profil;