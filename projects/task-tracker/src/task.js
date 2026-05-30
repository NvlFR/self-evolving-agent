const { v4: uuidv4 } = require('uuid');

class Task {
  constructor({ id = uuidv4(), description, status = 'pending', createdAt = new Date() }) {
    this.id = id;
    this.description = description;
    this.status = status;
    this.createdAt = createdAt;
  }

  static create(description, status = 'pending') {
    return new Task({ description, status });
  }

  delete() {
    this.status = 'deleted';
    return this;
  }

  toJSON() {
    return {
      id: this.id,
      description: this.description,
      status: this.status,
      createdAt: this.createdAt
    };
  }
}

module.exports = Task;