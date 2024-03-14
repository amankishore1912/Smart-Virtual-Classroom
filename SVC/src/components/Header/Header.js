import React from 'react'
import { useStyles } from './style'
import { AppBar, Avatar, Menu, MenuItem, Toolbar, Typography, Button, Box } from '@material-ui/core';
import { Add, Apps } from '@material-ui/icons';
import { CreateClass, JoinClass } from '..';
import { useLocalContext } from '../../context/context';



const Header = ({ children }) => {
    const classes = useStyles();

    const [anchorEl, setAnchorEl] = React.useState(null);
    const handleClick = (event) => setAnchorEl(event.currentTarget);
    const handleClose = () => setAnchorEl(null);

    const { setCreateClassDialog, setJoinClassDialog, loggedInUser, logout } = useLocalContext();

    const handleCreate = () => {
        handleClose();
        setCreateClassDialog(true);
    };

    const handleJoin = () => {
        handleClose();
        setJoinClassDialog(true);
    }

    const newTab = url=>{
        window.open(url)
    }

    return (
        <div className={classes.root}>
            <AppBar className={classes.appBar} color='white' position='static'>
                <Toolbar className={classes.toolbar}>
                    <div className={classes.headerWrapper}>
                        {children}
                        {/* <img
                            src="https://www.gstatic.com/images/branding/googlelogo/svg/googlelogo_clr_74x24px.svg"
                            alt="Classroom"
                        /> */}
                        <Typography variant="h6" className={classes.title}>
                            EduSphere
                        </Typography>
                    </div>

                    <div className={classes.header__wrapper__right}>
                        <Box marginRight={2}>

                            <Button onClick={()=> newTab('https://amankishore1912.github.io/EduSphere-Live-Class/')} variant="contained" color="primary">
                                Live Class
                            </Button>
                        </Box>
                        <Box marginRight={1}>
                            <Add onClick={handleClick} className={classes.icon} />
                        </Box>
                        <Box marginRight={1}>
                            <Apps className={classes.icon} />
                        </Box>

                        <Box marginRight={1}>
                            <Avatar onClick={() => logout()} src={loggedInUser?.photoURL} className={classes.icon} />
                        </Box>
                        <Menu
                            id="simple-menu"
                            anchorEl={anchorEl}
                            keepMounted
                            open={Boolean(anchorEl)}
                            onClose={handleClose}
                        >
                            <MenuItem onClick={handleJoin}>Join Class</MenuItem>
                            <MenuItem onClick={handleCreate}>Create Class</MenuItem>
                        </Menu>



                        {/* <div>
                            <Avatar onClick={() => logout()} src={loggedInUser?.photoURL} className={classes.icon} />
                        </div> */}


                    </div>
                </Toolbar>
            </AppBar>
            <CreateClass />
            <JoinClass />
        </div>
    )
}

export default Header
