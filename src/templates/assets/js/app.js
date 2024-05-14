import React from "react";
import ReactDOM from "react-dom";
import CreateProduct from "./components/CreateProduct";
import DetailProduct from "./components/DetailProduct";

// require('./bootstrap');
// require('./sb-admin');

const propsContainer = document.getElementById("variants");
let props = Object.assign({}, propsContainer.dataset);



ReactDOM.render(
    <React.StrictMode>
        <CreateProduct {...props}/>
    </React.StrictMode>,
    document.getElementById('root')
);

const propsProduct = document.getElementById("product");
props = Object.assign({}, propsProduct.dataset);


ReactDOM.render(
    <React.StrictMode>
        <DetailProduct {...props}/>
    </React.StrictMode>,
    document.getElementById('detail')
);
