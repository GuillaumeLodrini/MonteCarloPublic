'use strict'

import React from 'react'
import { render } from 'react-dom'

class CmsEdit extends React.Component {
    constructor(props) {
        super(props);
        this.changed = false;
    }

    onChanged = (e) => {
        this.content = e.target.innerText;
        this.changed = true;
    }

    send = (csrf_token) => {
        if (!this.changed)
            return;
        let data = new FormData();
        data.append('content', this.content);
        return fetch(window.location.origin+'/api/cms/'+this.props.token+'/',{
            method: 'PUT',
            body: data,
            headers:{
                'X-CSRFToken': csrf_token,
            }
        }).then(() => {
            this.changed = false;
        });
    }

    cancelEvents = (e) => {
        e.preventDefault();
    }

    render() {
        return (
            <span contentEditable onInput={this.onChanged} onClick={this.cancelEvents} suppressContentEditableWarning={true}>{this.props.value}</span>
        );
    }
}

class CmsSave extends React.Component {
    constructor(props) {
        super(props);
        this.fields = [];
        this.state = {
            sending: false,
        };
    }

    onPressed = (e) => {
        this.setState({sending: true});
        let promises = [];
        cms_fields.forEach(field => {
            promises.push(field.send(this.props.csrf_token));
        });
        Promise.all(promises).then(() => {
            this.setState({sending: false});
            alert("Les changements ont été enregistrés");
        });
    }

    render() {
        return (
            <button className="bouton bouton--primary" onClick={this.onPressed} disabled={this.state.sending}>{this.props.text}</button>
        );
    }
}

let cms_fields = [];

let registerField = (ref) => {
    cms_fields.push(ref);
}


document.querySelectorAll('.cms_edit').forEach(domContainer => {
    const token = domContainer.getAttribute("token");
    const value = domContainer.innerHTML;
    render(
        <CmsEdit value={value} token={token} ref={registerField}/>,
        domContainer
    );
});

let elementId = 'cms_save'
if (document.getElementById(elementId)) {
    const csrf_token = document.getElementById(elementId).getAttribute("csrf_token");
    render(
        <CmsSave text={document.getElementById(elementId).innerText} csrf_token={csrf_token}/>,
        document.getElementById(elementId)
    );
}
