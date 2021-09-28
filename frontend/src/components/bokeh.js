import React from 'react';
import Card from '@mui/material';

class BokehParticle extends React.Component {
  constructor(props){
    super(props);
    this.update = this.update.bind(this);
    this.render = this.render.bind(this);
    this.fps = 5;
    this.state = {
      size: Math.random() * 40 + 60,
      color: `#${Math.round(Math.random() * 0xffffff).toString(16)}`,
      x: Math.random() * 800,
      y: Math.random() * 480,
      trajectory: Math.random() * 360,
      speed: (Math.random() * 0.5) + 1,
      opacity: 1,
      fadingIn: true,
      fadeFactor: (Math.random() * 0.01) + 0.01
    };
  }

  componentDidMount(){
    this.interval = setInterval(() => { this.update() }, 1000 / this.fps);
  }

  componentWillUnmount(){clearInterval(this.interval)}

  regen(){
    this.setState({
        size: Math.random() * 40 + 60,
	fadingIn: true,
        color: `#${Math.round(Math.random() * 0xffffff).toString(16)}`,
        x: Math.random() * 800,
        y: Math.random() * 480,
        trajectory: (Math.random() * 360 * Math.PI) / 180,
        speed: (Math.random() * 2) - 1,
        fadeFactor: (Math.random() * 0.01) + 0.01
    });
  }

  update() {
    this.setState({x: this.state.x + (this.state.speed * Math.cos(this.state.trajectory)),
                   y: this.state.y + (this.state.speed * Math.sin(this.state.trajectory))});
    if(this.state.fadingIn){
      this.setState({opacity: this.state.opacity + this.state.fadeFactor});
      if(this.state.opacity > 1.0){
        this.setState({fadingIn: false});
      }
    } else {
      this.setState({opacity: this.state.opacity - this.state.fadeFactor});
      if(this.state.opacity < 0){
        this.regen();
      }
    }
  }

  render() {
    const styles = {
      particle : {
        borderRadius: `${this.state.size}px`,
        width: `${this.state.size}px`,
        height: `${this.state.size}px`,
        left: "0px",
        top: "0px",
        backgroundColor: this.state.color,
        opacity: this.state.opacity,
        position: "absolute",
        transform: `translate(${this.state.x}px, ${this.state.y}px)`,
        filter: "blur(3px)"
      }
    };
    return(<div style={styles.particle}></div>);
  }
}

class BokehAnimation extends React.Component {
  constructor(props){
    super(props);
    this.count = 5;
    this.maxSize = 100;
    this.minSize = 10;
    this.fps = 1000;   
    this.state = {
      particles: new Array(this.count).fill(<BokehParticle/>)
    }
  }

  componentDidMount() {
    //var particles = []
    //for(var i = 0; i < this.count; i++){
      //particles.push(new BokehParticle());
    //}
    //this.setState({particles: particles});
    //setInterval(() => {
    //  console.log("Updating");
    //  for(var i = 0; i < this.state.particles.length; i++){
     //   console.log(this.state.particles[i])
      //  this.state.particles[i].update();
     // }
    //}, this.fps);
  }

  componentWillUnmount(){}

  render() {
    const styles = {
    };
    return(<div>{this.state.particles}</div>);
  }
}

export default BokehAnimation
