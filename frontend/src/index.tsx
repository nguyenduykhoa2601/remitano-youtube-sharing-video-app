import ReactDOM from 'react-dom/client'
import App from './App'

import 'antd/dist/antd.min.css'

import { Provider } from 'react-redux'
import store from './redux/store'
import React from 'react'

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement)
root.render(
  <Provider store={store}>
    <App />
  </Provider>
)
