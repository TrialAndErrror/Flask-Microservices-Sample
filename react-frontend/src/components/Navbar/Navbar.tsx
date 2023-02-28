import {Navbar, Nav} from 'rsuite';
import HomeIcon from '@rsuite/icons/legacy/Home';
import CogIcon from '@rsuite/icons/legacy/Cog';

type NavMenuProps = {
    setActive: Function
    active: string
}

const NavMenu = ({active, setActive}: NavMenuProps) => (
    <Navbar>
        <Navbar.Brand href="#">Devbox</Navbar.Brand>
        <Nav>
            <Nav.Item onClick={() => setActive("temperature")} active={active == "temperature"}>Temperature</Nav.Item>
            <Nav.Item onClick={() => setActive("calc")} active={active == "calc"}>Feeding Calc</Nav.Item>


        </Nav>
        {/*<Nav pullRight>*/}
        {/*    <Nav.Item icon={<CogIcon/>}>Settings</Nav.Item>*/}
        {/*</Nav>*/}
    </Navbar>
);


export {NavMenu as default}
