import { Component } from "react";
import "./NavbarStyles.css";
import { MenuItems } from "./MenuItems";
import logo from "../img/logo.png";

class Navbar extends Component {
render(){
    return(
        <nav id="NavbarItems">
           <div id="logo" >
           <img className="logonPer"src={logo}/>
           </div>
           <ul id="nav-menu">
                  {MenuItems.map((item,index)=>{
                     return(
                        <li key={index}>
                        <a className={item.cName} href={item.url}>{item.title}</a> 
                        </li>
                     )
                  })}
           </ul>
         </nav>
    )
}
}

export default Navbar;