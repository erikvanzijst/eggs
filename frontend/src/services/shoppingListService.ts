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
  static async fetchLists(): Promise<string[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/lists/`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const lists = await response.json();
      return lists;
    } catch (error) {
      console.error('Error fetching lists:', error);
      throw error;
    }
  }

  /**
   * Fetch all items from a specific list
   * @param {string} listName - Name of the list
   * @returns {Promise<string[]>} List of item names
   */
  static async fetchItems(listName: string): Promise<string[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/lists/${listName}/items/`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const items = await response.json();
      return items;
    } catch (error) {
      console.error(`Error fetching items for list ${listName}:`, error);
      throw error;
    }
  }

  /**
   * Create a new item in a list
   * @param {string} listName - Name of the list
   * @param {object} item - Item to create with name property
   * @returns {Promise<object>} Created item response
   */
  static async createItem(listName: string, item: {name: string}): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/lists/${listName}/items/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(item),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const createdItem = await response.json();
      return createdItem;
    } catch (error) {
      console.error(`Error creating item in list ${listName}:`, error);
      throw error;
    }
  }

  /**
   * Delete an item from a list
   * @param {string} listName - Name of the list
   * @param {string} itemName - Name of the item to delete
   * @returns {Promise<{message: string}>} Delete confirmation message
   */
  static async deleteItem(listName: string, itemName: string): Promise<{message: string}> {
    try {
      const response = await fetch(`${API_BASE_URL}/lists/${listName}/items/${itemName}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      return result;
    } catch (error) {
      console.error(`Error deleting item ${itemName} from list ${listName}:`, error);
      throw error;
    }
  }

  /**
   * Create a new list
   * @param {string} listName - Name of the list to create
   * @returns {Promise<object>} Created list response
   */
  static async createList(listName: string): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/lists/${listName}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const createdList = await response.json();
      return createdList;
    } catch (error) {
      console.error(`Error creating list ${listName}:`, error);
      throw error;
    }
  }

/**
    * Get an item from a list
    * @param {string} listName - Name of the list
    * @param {string} itemName - Name of the item to retrieve
    * @returns {Promise<object>} Item response
    */
   static async getItem(listName: string, itemName: string): Promise<any> {
     try {
       const response = await fetch(`${API_BASE_URL}/lists/${listName}/items/${itemName}`);
       if (!response.ok) {
         throw new Error(`HTTP error! status: ${response.status}`);
       }
       const item = await response.json();
       return item;
     } catch (error) {
       console.error(`Error getting item ${itemName} from list ${listName}:`, error);
       throw error;
     }
   }

   /**
    * Delete a list
    * @param {string} listName - Name of the list to delete
    * @returns {Promise<{message: string}>} Delete confirmation message
    */
   static async deleteList(listName: string): Promise<{message: string}> {
     try {
       const response = await fetch(`${API_BASE_URL}/lists/${listName}`, {
         method: 'DELETE',
       });
       if (!response.ok) {
         throw new Error(`HTTP error! status: ${response.status}`);
       }
       const result = await response.json();
       return result;
     } catch (error) {
       console.error(`Error deleting list ${listName}:`, error);
       throw error;
     }
   }
}

export default ShoppingListService;