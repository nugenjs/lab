// Using CDN hosted modules instead of bundling node_modules
// import React from 'react';
// import ReactDOM from 'react-dom';

class Simple extends React.Component {
    render() {
        // return <div>helo {this.props['name']}</div>
        // return React.createElement('div', null, 'Helo, ' + this.props.name + '!');
        return React.createElement('div', {
            style: {
                display: 'flex'
            }
        }, 
            React.createElement('div', { style: {
                display: 'inline-flex',
                fontWeight: '700',
                whiteSpaceCollapse: "preserve"
            } }, 'Helo '),
            React.createElement('p', {
                style: {
                    margin: 'unset'    
                }
            }, this.props.name),
            React.createElement('div', { style: {
                display: 'inline-flex',
                fontWeight: '700',
                whiteSpaceCollapse: "preserve"
            } }, ' !'),
        );
    }
}

ReactDOM.render(
    // <Greetings name='worl' />,                    
    React.createElement(Simple, { name : 'Worl' }),
    document.getElementById('root')
);

// // Instead of using onLoad, use defer on HTML script to wait until components
// // which waits until DOM is fully built first, async downloads the src, but 
// // before DOMContentLoaded is called
// window.onload(() => {
// });
