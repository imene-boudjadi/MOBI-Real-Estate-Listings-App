import { Component } from "react";
import "./FirstPage.css";
import ImagOne from '../img/PageOne.png';
import NavLogo from "../components/NavLogo";


class FirstPage extends Component {
render(){
    return(
 <>
  <NavLogo/>
  <div className="gnrl">
        <div className="gen1">
             <div className='descr'>
                   <h1>MOBI</h1> 
                   <h>Votre platforme favorite pour trouver l’immobilier qui <br></br> vous convient</h>    
             </div>
             <div className='buttons'> 
                 <button className='b1' >S'identifier</button>
                <button className='b2'>Créer un compte</button>
             </div> 
         </div> 
         <div className="imagOne">
         <img src={ImagOne}/>
         </div>
  </div>    
  </>
    )
}
}

export default FirstPage;