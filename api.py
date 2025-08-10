import json
import tls_requests
from data import globalheaders,load_cookies,dealQuery,chatMessageQuery,updateItemQuery

class KiokePlayerok:
    def __init__(self,cookies_file="cookies.json",username=None):
        self.cookies = load_cookies(cookies_file)
        self.api_url = "https://playerok.com/graphql"
        self.username = username
        self.id = self.get_user_id()
        
    def get_user_id(self):

        """ПОЛУЧЕНИЕ ДАННЫХ ОБ АККАУНТЕ,ПОЛУЧАЕТ И ВОЗВРАЩАЕТ ТОЛЬКО ID -  ДЛЯ ДРУГИХ ФУНКЦИЙ"""
        params = {
        "operationName": "user",
        "variables": json.dumps({"username":self.username}),
        "extensions": json.dumps({"persistedQuery":{"version":1,"sha256Hash":"6dff0b984047e79aa4e416f0f0cb78c5175f071e08c051b07b6cf698ecd7f865"}})
    }
        
        try:
            response = tls_requests.get(self.api_url,cookies=self.cookies,headers=globalheaders,params=params)
            try:
                data = response.json() # чтобы добавить какие-то еще данные можно переписать функцию,для просмотра нужных данных print(data) 
                id = data.get('data',{}).get('user',{})["id"]
                return id
            except Exception as e:
                print(f"Ошибка при считывании json ")
                raise Exception
        
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    def get_actual_deals(self):
        """ПРОСМОТР АКТИВНЫХ СДЕЛОК"""
        params = {
        "operationName": "countDeals",
        "variables": json.dumps({
            "filter": {
                "userId": self.id,
                "direction": "OUT",
                "status": ["PAID"]
            }
        }),
        "extensions": json.dumps({
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "1e2605594b38041bb7a5466a9cab994a169725d7b69aae3b7ee185d0b7fc33c2"
            }
        })
    }

        try:
            response = tls_requests.get(self.api_url,cookies=self.cookies,headers=globalheaders,params=params)
            data = response.json()
            countDeals = data.get("data",{}).get("countDeals","")
            return countDeals
        except Exception as e:
            print(f"Ошибка при получении актуальных сделок: {e}")
            return None
        
    def get_info_from_deal(self):

        """получает информацию о вашей новой сделке которая есть в https://playerok.com/profile/вашникнаплеерке/sales"""
        params = {
            "operationName": "deals",
            "variables": json.dumps({"pagination":{"first":6},"filter":{"userId":self.id,"direction":"OUT","status":["PAID"]},"showForbiddenImage":True}),
            "extensions": json.dumps({"persistedQuery":{"version":1,"sha256Hash":"c3b623b5fe0758cf91b2335ebf36ff65f8650a6672a792a3ca7a36d270d396fb"}})
        }
        try:
            response = tls_requests.get(self.api_url,cookies=self.cookies,headers=globalheaders,params=params)
            data = response.json() #все данные можете посмотреть здесь
            deal_id = data.get("data",{}).get("deals",{}).get("edges",{})[0].get("node",{})["id"]
            buyer_name = data.get("data",{}).get("deals",{}).get("edges",{})[0].get("node",{}).get("user",{})["username"]
            bought_item_price = data.get("data",{}).get("deals",{}).get("edges",{})[0].get("node",{}).get("item",{})["price"]
            bought_item_name = data.get("data",{}).get("deals",{}).get("edges",{})[0].get("node",{}).get("item",{})["name"] #нужно для data_for_update_item
            return deal_id,buyer_name,bought_item_price,bought_item_name
        except Exception as e:
            print(f"Ошибка при получении данных о новой сделке: {e}")
            return None
        
    def get_data_from_deal_page(self,*,deal_id:str):
        """получает информацию о вашей активной сделке которая есть в https://playerok.com/deal/idсделки
        возвращает чат айди с покупателем в данной сделке и данные во вкладке: Получение если их нет возвращает None"""
        params = {
            "operationName": "deal",
            "variables": json.dumps({"id":deal_id,"showForbiddenImage":True}),
            "extensions": json.dumps({"persistedQuery":{"version":1,"sha256Hash":"54e7728119660a25de9193f51c347bb6ff574cab1c4137cfeaf83d42c7a05d2c"}})
        }
        try:
            response = tls_requests.get(self.api_url,cookies=self.cookies,headers=globalheaders,params=params)
            data = response.json() #все данные можете посмотреть здесь
            chat_id = data.get("data",{}).get("deal",{}).get("chat",{})["id"]
            obtainingfields = data.get("data",{}).get("deal",{}).get("obtainingFields",{})
            if not obtainingfields:
                print("Дополнительных данных при покупке не было указано")
            else:
                obtainingfields = data.get("data",{}).get("deal",{}).get("obtainingFields",{})[0]["value"]
                print("Дополнительные данные при покупке получены")
            return chat_id,obtainingfields
        except Exception as e:
            print(f"Ошибка при получении данных о новой сделке: {e}")
            return None
    
    def sendChatMessage(self,*,chatmessage:str,chatId:str):
        """ОТПРАВЛЯЕТ УКАЗАННОЕ СООБЩЕНИЕ  ПО УКАЗАННОМУ CHATID """
        json_data = {
            "operationName": "createChatMessage",
            "variables": {
                "input": {
                    "chatId": chatId, # принимает какой-то chatId
                    "text": chatmessage # текст соотвестенно
                }
            },
            "query":chatMessageQuery
        }
        try:
            tls_requests.post(self.api_url,cookies=self.cookies,headers=globalheaders,json=json_data)
            return True
            
        except Exception as e:
            print(f"Ошибка при отправлении сообщения: {e}")
            return False

    def manipulateDeal(self,*,status:str,deal_id:str):
        """Манипуляция со сделкой,вы можете указать два статуса: SENT ИЛИ ROLLED_BACK, означать они будут подтвердить или вернуть деньги соотвественно.
        Также обязательно нужно указать айди сделки"""
        json_data = {
            "operationName": "updateDeal",
            "variables":{        
                "input": {
                    "id": deal_id,
                    "status": status #SENT ИЛИ #ROLLED_BACK
                }
                },
            "query":dealQuery
        }
        try:
           tls_requests.post(self.api_url,cookies=self.cookies,headers=globalheaders,json=json_data)
           return True
        except Exception as e:
            print(f"Ошибка при получении актуальных сделок: {e}")
            return False

        
    def updateItem(self,*,isPremium:bool,item_name:str,price:int):
        """Выставляет заново товар во вкладке: 'Завершенные', при вызове нужно указывать в isPremium булево значение Точное имя товара и его цену, 
        ВНИМАНИЕ ПО УМОЛЧАНИЮ СТОИТ  ОБЫЧНОЕ ПОДНЯТИЕ  ЕСЛИ ТОВАР УЖЕ БЫЛ ПРЕМИУМ ТО ОТПРАВИТЬ ЕГО КАК ДЕФОЛТНЫЙ, К СОЖАЛЕНИЮ НЕ ПОЛУЧИТСЯ"""
        def get_data_for_update_item():
            params = {
                "operationName": "items",
                "variables": json.dumps({"pagination":{"first":16},"filter":{"userId":self.id,"status":["DECLINED","BLOCKED","EXPIRED","SOLD","DRAFT"]},"showForbiddenImage":True}),
                "extensions": json.dumps({"persistedQuery":{"version":1,"sha256Hash":"c6226e255848fb8f8ba74a73c79d24626b94b64757ba42548ae08e5a425558b8"}})
            }
            try:
                response = tls_requests.get(self.api_url,cookies=self.cookies,headers=globalheaders,params=params)
                data = response.json()
                items = data.get("data",{}).get("items",{}).get("edges",{})
                try:
                    for item in items:
                        if item.get("node",{})["name"] == item_name:
                            current_item_id = item.get("node",{})["id"]
                    return current_item_id
                
                except Exception as e:
                    print(f"Ошибка:{e} при считывании данных{items}")
                    raise Exception
            except Exception as e:
                print(f"Ошибка:  {e} при получении данных о текущем товаре с именем:{item_name}")
                return None
            
        itemId = get_data_for_update_item()
        def getIds():
            params = {
                "operationName": "itemPriorityStatuses",
                "variables": json.dumps({"itemId":itemId,"price":price}), 
                "extensions": json.dumps({"persistedQuery":{"version":1,"sha256Hash":"b922220c6f979537e1b99de6af8f5c13727daeff66727f679f07f986ce1c025a"}})
            }
            try:
                response = tls_requests.get(self.api_url,cookies=self.cookies,headers=globalheaders,params=params)
                data = response.json()
                try:
                    not_premium_id = data.get("data",{}).get("itemPriorityStatuses",{})[1]["id"] # сделать цикл 
                    premium_id = data.get("data",{}).get("itemPriorityStatuses",{})[0]["id"]
                    return not_premium_id,premium_id
                        
                # на самом деле можно ограничиться только одним айди товара но я думаю слаг будет не лишним
                except Exception as e:
                    print(f"Ошибка:{e} при считывании данных")
                    raise Exception
            except Exception as e:
                print(f"Ошибка:  {e} при получении данных об айди prem и non-prem поднятий")
                return None
            
        ids = getIds()
        not_premium_id,premium_id = ids
        finalStatus = not_premium_id
        if isPremium:
            finalStatus = premium_id       
        json_data = {
            "operationName": "publishItem",
            "variables": {
                "input": {
                    "transactionProviderId": "LOCAL",
                    "priorityStatuses": [
                     finalStatus
                    ],
                    "itemId": itemId 
                }
                },
                
            "query":updateItemQuery
        }
        try:
            tls_requests.post(self.api_url,cookies=self.cookies,headers=globalheaders,json=json_data)
            return True
            
        except Exception as e:
            print(f"Ошибка при выставлении : {e}")
            return False


#эти функции не для продаж они для серфинга 
    def fullCopyItem(self,*,slug:str,forReplace:bool):
        """ВНИМАНИЕ ФУНКЦИЯ ПО БОЛЬШЕЙ ЧАСТИ ДЛЯ ДРУГОЙ ФУНКЦИИ НО! ЕСЛИ ВЫ УКАЖИТЕ forReplace КАК FALSE ТО ВЕРНЕТСЯ ИМЯ,ОПИСАНИЕ,ЦЕНА,АВАТАРКА ТОВАРА"""
        params = {
            "operationName": "item",
            "variables": json.dumps({"slug":slug,"showForbiddenImage":True}),
            "extensions": json.dumps({"persistedQuery":{"version":1,"sha256Hash":"8a42e31376f38cd3052a578f0e719e5187191c0826058a8c7e5c2dc32e1a779d"}})
        }
        try:
            response = tls_requests.get(self.api_url,cookies=self.cookies,headers=globalheaders,params=params)
            data = response.json()
            copiedItem = data.get("data",{}).get("item",{})
            try:
                itemName = copiedItem["name"]
                description = copiedItem["description"]
                price = copiedItem["price"]
                itemAttributes = [itemName,price,description]
                
                
                comment = copiedItem.get("comment") 
                obtainingType = copiedItem.get("obtainingType")
                obtainingTypeId = None
                if obtainingType:
                    obtainingTypeId = obtainingType["id"]
                attributes = copiedItem.get("attributes")   
                categoryItemId = copiedItem.get("category").get("id")
                attachmentUrl = copiedItem["attachments"][0]["url"] #это обложка ее нужно указывать при копировании и айди
                attachmentId = copiedItem["attachments"][0]["id"] # id категории для функции выставления
                secondary = [comment,attributes,obtainingTypeId,categoryItemId]
                attachment = [attachmentUrl,attachmentId]
                                
                if not forReplace:
                    return itemAttributes,attachmentUrl 
                else:
                    return itemAttributes,secondary,attachment
                
            except Exception as e:
                print(f"Ошибка:{e} при считывании данных")
                raise Exception
            
        except Exception as e:
            print(f"Ошибка:  {e} при копировании товара с slug:{slug}")
            return None
    
    def placeItem(self,*, name:str, price:int, description:str, comment:str, game_category_id:str,attributes,obtainingTypeId:str,isPremium:bool):
        """функция в разработке главная проблема это корректное добавление через multiformdata изображения"""
        def getDataFields(): 
                dataFields = {
                "operationName": "gameCategoryDataFields",
                "variables": json.dumps({"pagination":{"first":20},"filter":{"gameCategoryId":game_category_id,"obtainingTypeId":obtainingTypeId,"type":"ITEM_DATA"}}),
                "extensions": json.dumps({"persistedQuery":{"version":1,"sha256Hash":"6fdadfb9b05880ce2d307a1412bc4f2e383683061c281e2b65a93f7266ea4a49"}})
                }
                response = tls_requests.get(self.api_url,cookies=self.cookies,headers=globalheaders,params=dataFields)
                data = response.json()
                dataFieldsIds = []
                dataContainers = data.get("data",{}).get("gameCategoryDataFields",{}).get("edges",{})
                for dataContainer in dataContainers:
                    dataFieldId = dataContainer.get("node",{}).get("id")
                    dataFieldsIds.append(dataFieldId)
                dictFields = []
                for id in  dataFieldsIds:
                    dictField = {}
                    dictField["fieldId"] = id
                    dictField["value"] = "made by kioke"
                    dictFields.append(dictField)

                return dictFields

        dataFields = getDataFields()

        def createPlaceID():
            json_data = {
            "operationName": "createItem",
            "variables": {
                "input": {
                    "gameCategoryId": game_category_id,
                    "name": name,
                    "price": price,
                    "description": description,
                    "comment": comment,
                    "obtainingTypeId":obtainingTypeId,
                    "attributes": attributes,
                    "dataFields": dataFields,
                },
                "attachments":[]
            },
            "query": "mutation createItem($input: CreateItemInput!, $attachments: [Upload!]!, $showForbiddenImage: Boolean) {\n  createItem(input: $input, attachments: $attachments) {\n    ...RegularItem\n    __typename\n  }\n}\n\nfragment RegularItem on Item {\n  ...RegularMyItem\n  ...RegularForeignItem\n  __typename\n}\n\nfragment RegularMyItem on MyItem {\n  ...ItemFields\n  prevPrice\n  priority\n  sequence\n  priorityPrice\n  statusExpirationDate\n  comment\n  viewsCounter\n  statusDescription\n  editable\n  statusPayment {\n    ...StatusPaymentTransaction\n    __typename\n  }\n  moderator {\n    id\n    username\n    __typename\n  }\n  approvalDate\n  deletedAt\n  createdAt\n  updatedAt\n  mayBePublished\n  prevFeeMultiplier\n  sellerNotifiedAboutFeeChange\n  __typename\n}\n\nfragment ItemFields on Item {\n  id\n  slug\n  name\n  description\n  rawPrice\n  price\n  attributes\n  status\n  priorityPosition\n  sellerType\n  feeMultiplier\n  user {\n    ...ItemUser\n    __typename\n  }\n  buyer {\n    ...ItemUser\n    __typename\n  }\n  attachments(showForbiddenImage: $showForbiddenImage) {\n    ...PartialFile\n    __typename\n  }\n  isAttachmentsForbidden\n  category {\n    ...RegularGameCategory\n    __typename\n  }\n  game {\n    ...RegularGameProfile\n    __typename\n  }\n  comment\n  dataFields {\n    ...GameCategoryDataFieldWithValue\n    __typename\n  }\n  obtainingType {\n    ...GameCategoryObtainingType\n    __typename\n  }\n  __typename\n}\n\nfragment ItemUser on UserFragment {\n  ...UserEdgeNode\n  __typename\n}\n\nfragment UserEdgeNode on UserFragment {\n  ...RegularUserFragment\n  __typename\n}\n\nfragment RegularUserFragment on UserFragment {\n  id\n  username\n  role\n  avatarURL\n  isOnline\n  isBlocked\n  rating\n  testimonialCounter\n  createdAt\n  supportChatId\n  systemChatId\n  __typename\n}\n\nfragment PartialFile on File {\n  id\n  url\n  __typename\n}\n\nfragment RegularGameCategory on GameCategory {\n  id\n  slug\n  name\n  categoryId\n  gameId\n  obtaining\n  options {\n    ...RegularGameCategoryOption\n    __typename\n  }\n  props {\n    ...GameCategoryProps\n    __typename\n  }\n  noCommentFromBuyer\n  instructionForBuyer\n  instructionForSeller\n  useCustomObtaining\n  autoConfirmPeriod\n  autoModerationMode\n  agreements {\n    ...RegularGameCategoryAgreement\n    __typename\n  }\n  feeMultiplier\n  __typename\n}\n\nfragment RegularGameCategoryOption on GameCategoryOption {\n  id\n  group\n  label\n  type\n  field\n  value\n  valueRangeLimit {\n    min\n    max\n    __typename\n  }\n  __typename\n}\n\nfragment GameCategoryProps on GameCategoryPropsObjectType {\n  minTestimonials\n  minTestimonialsForSeller\n  __typename\n}\n\nfragment RegularGameCategoryAgreement on GameCategoryAgreement {\n  description\n  gameCategoryId\n  gameCategoryObtainingTypeId\n  iconType\n  id\n  sequence\n  __typename\n}\n\nfragment RegularGameProfile on GameProfile {\n  id\n  name\n  type\n  slug\n  logo {\n    ...PartialFile\n    __typename\n  }\n  __typename\n}\n\nfragment GameCategoryDataFieldWithValue on GameCategoryDataFieldWithValue {\n  id\n  label\n  type\n  inputType\n  copyable\n  hidden\n  required\n  value\n  __typename\n}\n\nfragment GameCategoryObtainingType on GameCategoryObtainingType {\n  id\n  name\n  description\n  gameCategoryId\n  noCommentFromBuyer\n  instructionForBuyer\n  instructionForSeller\n  sequence\n  feeMultiplier\n  agreements {\n    ...MinimalGameCategoryAgreement\n    __typename\n  }\n  props {\n    minTestimonialsForSeller\n    __typename\n  }\n  __typename\n}\n\nfragment MinimalGameCategoryAgreement on GameCategoryAgreement {\n  description\n  iconType\n  id\n  sequence\n  __typename\n}\n\nfragment StatusPaymentTransaction on Transaction {\n  id\n  operation\n  direction\n  providerId\n  status\n  statusDescription\n  statusExpirationDate\n  value\n  props {\n    paymentURL\n    __typename\n  }\n  __typename\n}\n\nfragment RegularForeignItem on ForeignItem {\n  ...ItemFields\n  __typename\n}"
        }

            try:
                response = tls_requests.post(
                    self.api_url,
                    json=json_data,  
                    cookies=self.cookies,
                    headers=globalheaders
                )
                data = response.json()
                placeItemId = data.get("data",{}).get("createItem",{})["id"]
                return placeItemId
            
            except Exception as e:
                print(f"Ошибка createData {e}")
                return None
            
        kika = createPlaceID()
        print(kika)

        def getIds(*,itemId:str):
            params = {
                "operationName": "itemPriorityStatuses",
                "variables": json.dumps({"itemId":itemId,"price":price}), 
                "extensions": json.dumps({"persistedQuery":{"version":1,"sha256Hash":"b922220c6f979537e1b99de6af8f5c13727daeff66727f679f07f986ce1c025a"}})
            }
            try:
                response = tls_requests.get(self.api_url,cookies=self.cookies,headers=globalheaders,params=params)
                data = response.json()
                try:
                    not_premium_id = data.get("data",{}).get("itemPriorityStatuses",{})[1]["id"]
                    premium_id = data.get("data",{}).get("itemPriorityStatuses",{})[0]["id"]
                    return not_premium_id,premium_id

                except Exception as e:
                    print(f"Ошибка:{e} при считывании данных")
                    raise Exception
            except Exception as e:
                print(f"Ошибка:  {e} при получении данных об айди prem и non-prem поднятий")
                return None
            
        Item_temp_id = createPlaceID()
        ids = getIds(itemId=Item_temp_id)
        not_premium = ids[0]
        premium = ids[1]
        finalStatus = not_premium
        if isPremium:
            finalStatus = premium
        json_data = {
        "operationName": "publishItem",
        "variables": {
            "input": {
                "transactionProviderId": "LOCAL",
                "priorityStatuses": [
                    finalStatus
                ],
                "itemId":Item_temp_id
            }
            },
                
             "query":updateItemQuery
        }
        try:
            tls_requests.post(self.api_url,cookies=self.cookies,headers=globalheaders,json=json_data)
            return True
        
        except Exception as e:
            print(f"Ошибка при выставлении : {e}")
            return False
        

use = KiokePlayerok(cookies_file="cookies.json",username="KiokeSeller")



# op = use.fullCopyItem(slug="c5c25ad8d15b-propusk-polya-srazheniy-dazhe-rf-lyuboy-region",forReplace=True)
# itemName = op[0][0]
# itemPrice = op[0][1]
# itemDesc = op[0][2]
# comment = op[1][0]
# attr = op[1][1]
# obtaining = op[1][2]
# gaId = op[1][3]

# kik = use.placeItem(name=itemName,price=itemPrice,description=itemDesc,comment=comment,game_category_id=gaId,obtainingTypeId=obtaining,attributes=attr, isPremium=False)

# Доделать gameCategoryOptions просто список id с этими опциями и просмотреть другие товары что там может быть 
#при получении categoryId искать какие там могут быть obtainingfields