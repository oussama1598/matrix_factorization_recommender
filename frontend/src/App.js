import React from 'react';
import {Routes, Route} from "react-router-dom";
import NavBar from './components/NavBar';
import './App.css';
import UserList from "./pages/UserList";
import ItemsList from "./pages/ItemsList";

function App() {
    return (
        <div className="App">
            <NavBar/>
            <Routes>
                <Route path="/users" element={<UserList/>}/>
                <Route path="/items" element={<ItemsList/>}/>
            </Routes>
        </div>
    );
}

export default App;