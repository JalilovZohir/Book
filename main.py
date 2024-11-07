class Book:
    book_count = 0

    def __init__(self,title,author,janr,ishlab_chiqarilgan_yili,price,availability=True):
        self.title = title
        self.author = author
        self.janr = janr
        self.ishlab_chiqarilgan_yili = ishlab_chiqarilgan_yili
        self.__price = price
        self.__availability = availability
    def get_price(self):
        return f"{self.__price}$"
    def set_price(self,new_price):
        if new_price < 0:
            raise ValueError("Bu narxga bera olmaymiz!")
        self.__price = new_price
    def is_available(self):
        return self.__availability
    def set_available(self,new):
        self.__availability = new
    def desplay_details(self):
        return (
            f"Nomi: {self.title}, "
            f"Kim tomonidan yozilgani: {self.author}, "
            f"Janr: {self.janr}, "
            f"Ishlab chiqarilgan yili: {self.ishlab_chiqarilgan_yili}, "
            f"Puli: {self.__price}$, "
            f"Borligi: {'Ha' if self.__availability else "Yo\'q"}"
        )
    
    def discount_percentage(self,percent):
        if self.__availability :
            self.__price -= self.__price * (percent / 100 )
        else :
            return f"uzur, bu kitobdan hozir yo'q keyingi safar keladi"
    def mark_univailable(self):
        self.__availability = False
        return self.__availability
    
    def get_book_count (self):
        return Book.book_count