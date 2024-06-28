import { Component } from "react";
import "./NavLogo.css";
import logo from "../img/logo.png";


class NavLogo extends Component {
render(){
    return(
        <div className="Logo-Container">
           <img src={logo}/>
        </div>
    )
}
}
export default NavLogo;