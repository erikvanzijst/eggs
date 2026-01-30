import { APIError, ConflictError, NotFoundError } from '../exceptions';

// Base URL for the API - using the environment variable or default to localhost
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

/**
 * API service for shopping list operations
 */
class ShoppingListService {
  /**
   * Fetch all lists from the backend
   * @returns {Promise<string[]>} List of list names
   */
  static async getLists(): Promise<string[]> {
    const response = await fetch(`${API_BASE_URL}/lists/`);
    if (!response.ok) {
      throw new APIError(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  }

  /**
   * Fetch a specific list from the backend
   * @returns {string} the name of the list
   */
  static async getList(listName: string): Promise<string[]> {
    const response = await fetch(`${API_BASE_URL}/lists/${listName}`);
    if (response.status === 404) {
      throw new NotFoundError(listName);
    } else if (!response.ok) {
      throw new APIError(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  }

  /**
   * Create a new list
   * @param {string} listName - Name of the list to create
   * @returns {Promise<object>} Created list response
   */
  static async createList(listName: string): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/lists/${listName}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      if (response.status === 409) {
        throw new ConflictError("List already exists");
      } else {
        throw new APIError(`HTTP error! status: ${response.status}`);
      }
    }
    return await response.json();
  }

  /**
   * Fetch all items from a specific list
   * @param {string} listName - Name of the list
   * @returns {Promise<string[]>} List of item names
   */
  static async getItems(listName: string): Promise<string[]> {
    const response = await fetch(`${API_BASE_URL}/lists/${listName}/items/`);
    if (!response.ok) {
      if (response.status === 404) {
        throw new NotFoundError(`No such list: ${listName}`);
      } else {
        throw new APIError(`HTTP error! status: ${response.status}`);
      }
    }
    return await response.json();
  }

  /**
   * Create a new item in a list
   * @param {string} listName - Name of the list
   * @param {object} item - Item to create with name property
   * @returns {Promise<object>} Created item response
   */
  static async createItem(listName: string, item: {name: string}): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/lists/${listName}/items/${item.name}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(item),
    });
    if (!response.ok) {
      if (response.status === 409) {
        throw new ConflictError(`${item} already exists`);
      } else if (response.status === 404) {
        throw new NotFoundError(`No such list: ${listName}`);
      } else {
        throw new APIError(`HTTP error! status: ${response.status}`);
      }
    }
    return await response.json();
  }

  /**
   * Delete an item from a list
   * @param {string} listName - Name of the list
   * @param {string} itemName - Name of the item to delete
   * @returns {Promise<{message: string}>} Delete confirmation message
   */
  static async deleteItem(listName: string, itemName: string): Promise<{message: string}> {
    const response = await fetch(`${API_BASE_URL}/lists/${listName}/items/${itemName}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      if (response.status === 404) {
        throw new NotFoundError(`No such list/item: ${listName}/${itemName}`);
      } else {
        throw new APIError(`HTTP error! status: ${response.status}`);
      }
    }
    return await response.json();
  }

  /**
    * Get an item from a list
    * @param {string} listName - Name of the list
    * @param {string} itemName - Name of the item to retrieve
    * @returns {Promise<object>} Item response
    */
  static async getItem(listName: string, itemName: string): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/lists/${listName}/items/${itemName}`);
    if (!response.ok) {
      if (response.status === 404) {
        throw new NotFoundError(`No such list/item: ${listName}/${itemName}`);
      } else {
        throw new APIError(`HTTP error! status: ${response.status}`);
      }
    }
    return await response.json();
   }

   /**
    * Delete a list
    * @param {string} listName - Name of the list to delete
    */
   static async deleteList(listName: string) {
     const response = await fetch(`${API_BASE_URL}/lists/${listName}`, {
       method: 'DELETE',
     });
     if (!response.ok) {
       if (response.status === 404) {
         throw new NotFoundError(`No such list: ${listName}`);
       } else {
         throw new APIError(`HTTP error! status: ${response.status}`);
       }
     }
   }
}

export default ShoppingListService;