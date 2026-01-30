export class APIError extends Error {
  constructor(msg: string) {
    super(msg);
    Object.setPrototypeOf(this, APIError.prototype);
  }
}

export class NotFoundError extends APIError {
  constructor(msg: string) {
    super(msg);
    Object.setPrototypeOf(this, NotFoundError.prototype);
  }
}

export default { NotFoundError, APIError };
