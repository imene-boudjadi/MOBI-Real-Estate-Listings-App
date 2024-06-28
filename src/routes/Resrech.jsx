import React from "react"
import { useState } from "react"
import'bootstrap/dist/css/bootstrap.min.css';
import data from "../Source/data";
import "./Resrech.css"
import Card from 'react-bootstrap/Card';
import Navbar from "../components/Navbar";


const Resrech = () => {

  const [noOfElements,setnoOfElement]=useState(4);
  const slice = data.annonceData.slice(0,noOfElements);
  const afficherPlus = () =>{
    setnoOfElement(noOfElements+noOfElements);
  } 
  return (
    <>
      <Navbar/>
    <div className="main">
        <section className="py-4 py-lg-5 container">
                <div className="row justify-content-center align-item-center">
                    {slice.map((item,index)=>{
                        return(
                        <div className="col-11 col-md-6 col-lg-3 mx-0 mb-4" key={index}>
                              <Card className="annonce">
           
                                    <div className="image-an">
                                        <Card.Img src={item.img}/>
                                    </div>
                                    <Card.Body className="info-annonce">
                                        <Card.Title className="titre">{item.titre}</Card.Title>
                                        <Card.Title className="prix">{item.prix}</Card.Title>
                                        <Card.Title className="catego">{item.catego}</Card.Title>
                                        <Card.Title className="lieu">{item.lieu}</Card.Title>
                                        <div className="details">
                                                <button>Détails</button>
                                        </div>
                                        
                                    </Card.Body>
                                </Card>
                         </div>)
                    })}
                    
                </div>
                <button className="btn d-block w-100" onClick={()=> afficherPlus()}>Afficher Plus</button>
        </section>
  </div>
    </>
  )
}

export default Resrech