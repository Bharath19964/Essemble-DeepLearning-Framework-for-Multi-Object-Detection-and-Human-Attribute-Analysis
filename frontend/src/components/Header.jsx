import React from "react";

export default function Header() {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-white shadow-sm app-topbar">
      <div className="container">
        <span className="navbar-brand fw-bold app-brand">
          Ensemble Deep Learning Framework
        </span>

        <div className="collapse navbar-collapse show">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <a className="nav-link text-muted" href="#insights">Insights</a>
            </li>
            <li className="nav-item">
              <a className="nav-link text-muted" href="#about">About</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}