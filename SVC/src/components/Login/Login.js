import React from 'react'
import logo from "../../assets/logo1.png";
import { Button } from '@material-ui/core';
import "./style.css";
import { useLocalContext } from '../../context/context';

const Login = () => {
    const {login, loggedInUser} = useLocalContext();

    console.log(loggedInUser);

    return (
        <div className='login'>
            <img className="login__logo" src={logo} alt="Classroom" />
            <Button variant="contained" color="default" onClick={()=>login()}>
                Login Now!
            </Button>
        </div>
    );
};

export default Login
