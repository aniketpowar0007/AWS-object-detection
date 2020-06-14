import React, { Component,Fragment } from 'react';
import axios from 'axios';
import JSONPretty from 'react-json-pretty';

export default class Form extends Component {
  constructor(props) {
    super(props);
    this.state = {
      name: '',
      links: null,
      
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    const inputValue = event.target.value;
    const stateField = event.target.name;
    this.setState({
      [stateField]: inputValue,
    });
    console.log(this.state);
  }

  
  async handleSubmit(event) {
    event.preventDefault();
  
    const { name } = this.state;
    const headers = {'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST'};
    try{
    const response = await axios.post('https://cors-anywhere.herokuapp.com/' +
      'https://cut6nmdii3.execute-api.us-east-1.amazonaws.com/production',
      { tags: `${name}`.split(",") }, {headers}
    )
    //const data = response.json();
    this.setState({links: response.request.response})
    console.log(response.request.response);
    
    }
    
    catch (error) {
        
       
    }
}

  render() {
      
    return (
        <Fragment>
                <form>
                {this.props.auth.isAuthenticated && this.props.auth.user && (
                    <div className="container mt-4">
                    <h1 className="display-4 text-center mb-4">
                    <i className=" fa-react"/><b>Enter Tags to get a list of URLS</b> </h1>

                    <div className="container mt-4">
                    <label for="exampleInputEmail1"></label>
                    <form onSubmit={this.handleSubmit}>
                    <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter Tags" type="text" name="name" onChange={this.handleChange} value={this.state.name}/>
                    <small id="emailHelp" class="form-text text-muted">For multiple tags enter comma after every tag. eg "car,person"</small>
                    <input type="submit" value="Send Query" className="container btn btn-primary btn-block mt-4" />
                    
     
          
                    </form>
                
                </div>

        
    <div> <JSONPretty id="json-pretty" data={this.state.links}></JSONPretty></div>
          
      
     </div>
                )}
     </form>
     </Fragment>
    );
  }
}