import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Redirect, Switch, useLocation } from "react-router-dom";
import "./app.css";
import { ArtGallery } from "../ArtGallery/ArtGallery";
import { Login } from "../components/Login";
import { Register } from "../components/Register";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("token"));

  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token);
  }, []);

  return (
    <Router basename="/">
      <Switch>
        <Route exact path="/">
          {isLoggedIn ? (
            <ArtGalleryPage onLogout={() => setIsLoggedIn(false)} />
          ) : (
            <Redirect to="/login" />
          )}
        </Route>
        <Route path="/login">
          <Login onLoginSuccess={() => setIsLoggedIn(true)} />
        </Route>
        <Route path="/register" component={Register} />
        <Redirect to="/" />
      </Switch>
    </Router>
  );
}

function ArtGalleryPage({ onLogout }) {
  const handleLogout = () => {
    localStorage.removeItem("token");
    onLogout();
    window.location.href = "/login";
  };

  return (
    <div className="App">
      <div className="top-right-controls">
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </div>
      <ArtGallery windowWidth={window.innerWidth} />
    </div>
  );
}

export default App;
