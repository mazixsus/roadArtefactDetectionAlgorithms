import React from 'react';
import '../styles/App.css';
import Dashboard from "./Dashboard";
import {connect} from "react-redux";
import {surveysInfoFetched} from "../redux/actions";


export function App() {


  return (
    <div className="App">
      <Dashboard/>
    </div>
  );
}

const mapStateToProps = (state) => {
    return {
        surveysInfo: state.surveysInfo
    }
};
const mapDispatchToProps = {surveysInfoFetched};

export const AppContainer = connect(mapStateToProps, mapDispatchToProps)(App);
