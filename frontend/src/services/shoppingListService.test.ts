import ShoppingListService from './shoppingListService';
import NotFoundError from '../exceptions';

// Mock fetch globally for testing
global.fetch = jest.fn();

describe('ShoppingListService', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  describe('fetchLists', () => {
    it('should fetch lists successfully', async () => {
      const mockLists = ['Groceries', 'To-Do', 'Shopping'];
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: jest.fn().mockResolvedValue(mockLists)
      });

      const lists = await ShoppingListService.getLists();
      expect(lists).toEqual(mockLists);
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/v1/lists/');
    });

    it('should throw an error when fetch fails', async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500
      });

      await expect(ShoppingListService.getLists()).rejects.toThrow('HTTP error! status: 500');
    });
  });

  describe('fetchItems', () => {
    it('should fetch items successfully', async () => {
      const listName = 'Groceries';
      const mockItems = ['Milk', 'Bread', 'Eggs'];
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: jest.fn().mockResolvedValue(mockItems)
      });

      const items = await ShoppingListService.getItems(listName);
      expect(items).toEqual(mockItems);
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/v1/lists/Groceries/items/');
    });

    it('should throw an error when fetch items fails', async () => {
      const listName = 'Groceries';
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500
      });

      await expect(ShoppingListService.getItems(listName)).rejects.toThrow('HTTP error! status: 500');
    });
  });

  describe('createItem', () => {
it('should create an item successfully', async () => {
       const listName = 'Groceries';
       const item = { name: 'Cheese' };
       const mockCreatedItem = { id: 1, name: 'Cheese' };
       (global.fetch as jest.Mock).mockResolvedValueOnce({
         ok: true,
         json: jest.fn().mockResolvedValue(mockCreatedItem)
       });

       const createdItem = await ShoppingListService.createItem(listName, item);
       expect(createdItem).toEqual(mockCreatedItem);
       expect(global.fetch).toHaveBeenCalledWith(
         'http://localhost:8000/api/v1/lists/Groceries/items/Cheese',
         {
           method: 'POST',
           headers: {
             'Content-Type': 'application/json',
           },
           body: JSON.stringify(item),
         }
       );
     });

    it('should throw an error when creating item fails', async () => {
      const listName = 'Groceries';
      const item = { name: 'Cheese' };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500
      });

      await expect(ShoppingListService.createItem(listName, item)).rejects.toThrow('HTTP error! status: 500');
    });
  });

  describe('deleteItem', () => {
    it('should delete an item successfully', async () => {
      const listName = 'Groceries';
      const itemName = 'Milk';
      const mockResult = { message: 'Item deleted successfully' };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: jest.fn().mockResolvedValue(mockResult)
      });

      const result = await ShoppingListService.deleteItem(listName, itemName);
      expect(result).toEqual(mockResult);
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/v1/lists/Groceries/items/Milk', {
        method: 'DELETE'
      });
    });

    it('should throw an error when deleting item fails', async () => {
      const listName = 'Groceries';
      const itemName = 'Milk';
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500
      });

      await expect(ShoppingListService.deleteItem(listName, itemName)).rejects.toThrow('HTTP error! status: 500');
    });
  });

  describe('createList', () => {
    it('should create a list successfully', async () => {
      const listName = 'New List';
      const mockCreatedList = { name: 'New List', id: 1 };
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: jest.fn().mockResolvedValue(mockCreatedList)
      });

      const createdList = await ShoppingListService.createList(listName);
      expect(createdList).toEqual(mockCreatedList);
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/lists/New List',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        }
      );
    });

    it('should throw an error when creating list fails', async () => {
      const listName = 'New List';
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500
      });

      await expect(ShoppingListService.createList(listName)).rejects.toThrow('HTTP error! status: 500');
    });
  });

describe('deleteList', () => {
     it('should delete a list successfully', async () => {
       const listName = 'To-Do';
       const mockResult = { message: 'List deleted successfully' };
       (global.fetch as jest.Mock).mockResolvedValueOnce({
         ok: true,
         json: jest.fn().mockResolvedValue(mockResult)
       });

       await ShoppingListService.deleteList(listName);
       expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/v1/lists/To-Do', {
         method: 'DELETE'
       });
     });

     it('should throw an error when deleting list fails', async () => {
       const listName = 'To-Do';
       (global.fetch as jest.Mock).mockResolvedValueOnce({
         ok: false,
         status: 500
       });

       await expect(ShoppingListService.deleteList(listName)).rejects.toThrow('HTTP error! status: 500');
     });
   });

   describe('getItem', () => {
     it('should get an item successfully', async () => {
       const listName = 'Groceries';
       const itemName = 'Milk';
       const mockItem = { id: 1, list_id: 1, name: 'Milk' };
       (global.fetch as jest.Mock).mockResolvedValueOnce({
         ok: true,
         json: jest.fn().mockResolvedValue(mockItem)
       });

       const item = await ShoppingListService.getItem(listName, itemName);
       expect(item).toEqual(mockItem);
       expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/v1/lists/Groceries/items/Milk');
     });

     it('should throw an error when getting item fails', async () => {
       const listName = 'Groceries';
       const itemName = 'Milk';
       (global.fetch as jest.Mock).mockResolvedValueOnce({
         ok: false,
         status: 404
       });

       await expect(ShoppingListService.getItem(listName, itemName)).rejects.toThrow(NotFoundError);
     });
   });
});