
import Navbar from "../components/Navbar";
import './Acceuil.css';
import React, { useState } from "react";

export const Acceuil = () => {
    const  [filtre,setFiltre]=useState('Entrer vos mots clefs');  
    return (
    <>          
           <Navbar/>
           <div className="AddandSrch">
                <button id="add-an" type="button">Publier votre annonce</button>
                <div className="srch">
                        <div className="Filter">
                                
                                        <select data-trigger="" placeholder="Filtre"className="Filter-real" >
                                            <option>Type</option>
                                            <option>Wilaya</option>
                                            <option>Commune</option>
                                            <option>Période</option>
                                        </select>
                            
                        </div>
                        <div className="Search">
                            <input type="text" placeholder={filtre}/>
                        </div>
                        <div className="Search-icon">
                            <button type="button">Rechercher</button>
                        </div>
                           
                </div>
           </div>
        </>
    )
}
export default Acceuil;