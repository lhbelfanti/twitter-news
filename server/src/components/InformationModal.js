import React, { Component } from 'react';
import { Button, Modal } from 'semantic-ui-react';
import ModalList from './ModalList';


class InformationModal extends Component {

  render() {
    const { buttonStyle } = styles;

    const { title,
      url,
    } = this.props.data;


    return (
      <Modal trigger={<Button color='twitter' style={buttonStyle}>Más información</Button>}>
        <Modal.Header><a href={url}>{title}</a></Modal.Header>
        <Modal.Content>
          <ModalList data={this.props.data} />
        </Modal.Content>
      </Modal>
    );
  }
}

const styles = {
  buttonStyle: {
    marginTop: 20,
    width: 200
  }
};

export default InformationModal;