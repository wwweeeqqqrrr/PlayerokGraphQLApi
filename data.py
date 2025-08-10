import json

globalheaders = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'access-control-allow-headers': 'sentry-trace, baggage',
    'apollo-require-preflight': 'true',
    'apollographql-client-name': 'web',
    'content-type': 'application/json',
    'origin': 'https://playerok.com',
    'priority': 'u=1, i',
    'referer': 'https://playerok.com/profile/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"135.0.7049.115"',
    'sec-ch-ua-full-version-list': '"Google Chrome";v="135.0.7049.115", "Not-A.Brand";v="8.0.0.0", "Chromium";v="135.0.7049.115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"19.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-timezone-offset': '-180',
}
def load_cookies(cookies_file):
        cookies_dict = {}
        try:
            with open(cookies_file, "r", encoding="utf-8") as file:
                cookies = json.load(file)
                for cookie in cookies:
                    cookies_dict[cookie["name"]] = cookie["value"]
        except Exception as e:
            print(f"Ошибка при загрузке куков: {e}")
        return cookies_dict

dealQuery = """mutation updateDeal($input: UpdateItemDealInput!, $showForbiddenImage: Boolean) {
  updateDeal(input: $input) {
    ...RegularItemDeal
    __typename
  }
}

fragment RegularItemDeal on ItemDeal {
  id
  status
  direction
  statusExpirationDate
  statusDescription
  obtaining
  hasProblem
  reportProblemEnabled
  completedBy {
    ...MinimalUserFragment
    __typename
  }
  props {
    ...ItemDealProps
    __typename
  }
  prevStatus
  completedAt
  createdAt
  logs {
    ...ItemLog
    __typename
  }
  transaction {
    ...ItemDealTransaction
    __typename
  }
  user {
    ...UserEdgeNode
    __typename
  }
  chat {
    ...RegularChatId
    __typename
  }
  item {
    ...PartialDealItem
    __typename
  }
  testimonial {
    ...RegularItemDealTestimonial
    __typename
  }
  obtainingFields {
    ...GameCategoryDataFieldWithValue
    __typename
  }
  commentFromBuyer
  __typename
}

fragment MinimalUserFragment on UserFragment {
  id
  username
  role
  __typename
}

fragment ItemDealProps on ItemDealProps {
  autoConfirmPeriod
  __typename
}

fragment ItemLog on ItemLog {
  id
  event
  createdAt
  user {
    ...UserEdgeNode
    __typename
  }
  __typename
}

fragment UserEdgeNode on UserFragment {
  ...RegularUserFragment
  __typename
}

fragment RegularUserFragment on UserFragment {
  id
  username
  role
  avatarURL
  isOnline
  isBlocked
  rating
  testimonialCounter
  createdAt
  supportChatId
  systemChatId
  __typename
}

fragment ItemDealTransaction on Transaction {
  id
  operation
  direction
  providerId
  status
  value
  createdAt
  paymentMethodId
  statusExpirationDate
  __typename
}

fragment RegularChatId on Chat {
  id
  __typename
}

fragment PartialDealItem on Item {
  ...PartialDealMyItem
  ...PartialDealForeignItem
  __typename
}

fragment PartialDealMyItem on MyItem {
  id
  slug
  priority
  status
  name
  price
  priorityPrice
  rawPrice
  statusExpirationDate
  sellerType
  approvalDate
  createdAt
  priorityPosition
  viewsCounter
  feeMultiplier
  comment
  attachments(showForbiddenImage: $showForbiddenImage) {
    ...RegularFile
    __typename
  }
  isAttachmentsForbidden
  user {
    ...UserEdgeNode
    __typename
  }
  game {
    ...RegularGameProfile
    __typename
  }
  category {
    ...MinimalGameCategory
    __typename
  }
  dataFields {
    ...GameCategoryDataFieldWithValue
    __typename
  }
  obtainingType {
    ...MinimalGameCategoryObtainingType
    __typename
  }
  __typename
}

fragment RegularFile on File {
  id
  url
  filename
  mime
  __typename
}

fragment RegularGameProfile on GameProfile {
  id
  name
  type
  slug
  logo {
    ...PartialFile
    __typename
  }
  __typename
}

fragment PartialFile on File {
  id
  url
  __typename
}

fragment MinimalGameCategory on GameCategory {
  id
  slug
  name
  __typename
}

fragment GameCategoryDataFieldWithValue on GameCategoryDataFieldWithValue {
  id
  label
  type
  inputType
  copyable
  hidden
  required
  value
  __typename
}

fragment MinimalGameCategoryObtainingType on GameCategoryObtainingType {
  id
  name
  description
  gameCategoryId
  noCommentFromBuyer
  instructionForBuyer
  instructionForSeller
  sequence
  feeMultiplier
  props {
    minTestimonialsForSeller
    __typename
  }
  __typename
}

fragment PartialDealForeignItem on ForeignItem {
  id
  slug
  priority
  status
  name
  price
  rawPrice
  sellerType
  approvalDate
  priorityPosition
  createdAt
  viewsCounter
  feeMultiplier
  comment
  attachments(showForbiddenImage: $showForbiddenImage) {
    ...RegularFile
    __typename
  }
  isAttachmentsForbidden
  user {
    ...UserEdgeNode
    __typename
  }
  game {
    ...RegularGameProfile
    __typename
  }
  category {
    ...MinimalGameCategory
    __typename
  }
  dataFields {
    ...GameCategoryDataFieldWithValue
    __typename
  }
  obtainingType {
    ...MinimalGameCategoryObtainingType
    __typename
  }
  __typename
}

fragment RegularItemDealTestimonial on Testimonial {
  id
  status
  text
  rating
  createdAt
  updatedAt
  creator {
    ...RegularUserFragment
    __typename
  }
  moderator {
    ...RegularUserFragment
    __typename
  }
  user {
    ...RegularUserFragment
    __typename
  }
  __typename
}
    """
chatMessageQuery = """mutation createChatMessage($input: CreateChatMessageInput!, $file: Upload, $showForbiddenImage: Boolean) {
    createChatMessage(input: $input, file: $file) {
        ...RegularChatMessage
        __typename
    }
    }

    fragment RegularChatMessage on ChatMessage {
    id
    text
    createdAt
    deletedAt
    isRead
    isSuspicious
    isBulkMessaging
    game {
        ...RegularGameProfile
        __typename
    }
    file {
        ...PartialFile
        __typename
    }
    user {
        ...ChatMessageUserFields
        __typename
    }
    deal {
        ...ChatMessageItemDeal
        __typename
    }
    item {
        ...ItemEdgeNode
        __typename
    }
    transaction {
        ...RegularTransaction
        __typename
    }
    moderator {
        ...UserEdgeNode
        __typename
    }
    eventByUser {
        ...ChatMessageUserFields
        __typename
    }
    eventToUser {
        ...ChatMessageUserFields
        __typename
    }
    isAutoResponse
    event
    buttons {
        ...ChatMessageButton
        __typename
    }
    __typename
    }

    fragment RegularGameProfile on GameProfile {
    id
    name
    type
    slug
    logo {
        ...PartialFile
        __typename
    }
    __typename
    }

    fragment PartialFile on File {
    id
    url
    __typename
    }

    fragment ChatMessageUserFields on UserFragment {
    ...UserEdgeNode
    __typename
    }

    fragment UserEdgeNode on UserFragment {
    ...RegularUserFragment
    __typename
    }

    fragment RegularUserFragment on UserFragment {
    id
    username
    role
    avatarURL
    isOnline
    isBlocked
    rating
    testimonialCounter
    createdAt
    supportChatId
    systemChatId
    __typename
    }

    fragment ChatMessageItemDeal on ItemDeal {
    id
    direction
    status
    statusDescription
    hasProblem
    user {
        ...ChatParticipant
        __typename
    }
    testimonial {
        ...ChatMessageDealTestimonial
        __typename
    }
    item {
        id
        name
        price
        slug
        rawPrice
        sellerType
        user {
        ...ChatParticipant
        __typename
        }
        category {
        id
        __typename
        }
        attachments(showForbiddenImage: $showForbiddenImage) {
        ...PartialFile
        __typename
        }
        isAttachmentsForbidden
        comment
        dataFields {
        ...GameCategoryDataFieldWithValue
        __typename
        }
        obtainingType {
        ...GameCategoryObtainingType
        __typename
        }
        __typename
    }
    obtainingFields {
        ...GameCategoryDataFieldWithValue
        __typename
    }
    chat {
        id
        type
        __typename
    }
    transaction {
        id
        statusExpirationDate
        __typename
    }
    statusExpirationDate
    commentFromBuyer
    __typename
    }

    fragment ChatParticipant on UserFragment {
    ...RegularUserFragment
    __typename
    }

    fragment ChatMessageDealTestimonial on Testimonial {
    id
    status
    text
    rating
    createdAt
    updatedAt
    creator {
        ...RegularUserFragment
        __typename
    }
    moderator {
        ...RegularUserFragment
        __typename
    }
    user {
        ...RegularUserFragment
        __typename
    }
    __typename
    }

    fragment GameCategoryDataFieldWithValue on GameCategoryDataFieldWithValue {
    id
    label
    type
    inputType
    copyable
    hidden
    required
    value
    __typename
    }

    fragment GameCategoryObtainingType on GameCategoryObtainingType {
    id
    name
    description
    gameCategoryId
    noCommentFromBuyer
    instructionForBuyer
    instructionForSeller
    sequence
    feeMultiplier
    agreements {
        ...MinimalGameCategoryAgreement
        __typename
    }
    props {
        minTestimonialsForSeller
        __typename
    }
    __typename
    }

    fragment MinimalGameCategoryAgreement on GameCategoryAgreement {
    description
    iconType
    id
    sequence
    __typename
    }

    fragment ItemEdgeNode on ItemProfile {
    ...MyItemEdgeNode
    ...ForeignItemEdgeNode
    __typename
    }

    fragment MyItemEdgeNode on MyItemProfile {
    id
    slug
    priority
    status
    name
    price
    rawPrice
    statusExpirationDate
    sellerType
    attachment(showForbiddenImage: $showForbiddenImage) {
        ...PartialFile
        __typename
    }
    isAttachmentsForbidden
    user {
        ...UserItemEdgeNode
        __typename
    }
    approvalDate
    createdAt
    priorityPosition
    viewsCounter
    feeMultiplier
    __typename
    }

    fragment UserItemEdgeNode on UserFragment {
    ...UserEdgeNode
    __typename
    }

    fragment ForeignItemEdgeNode on ForeignItemProfile {
    id
    slug
    priority
    status
    name
    price
    rawPrice
    sellerType
    attachment(showForbiddenImage: $showForbiddenImage) {
        ...PartialFile
        __typename
    }
    isAttachmentsForbidden
    user {
        ...UserItemEdgeNode
        __typename
    }
    approvalDate
    priorityPosition
    createdAt
    viewsCounter
    feeMultiplier
    __typename
    }

    fragment RegularTransaction on Transaction {
    id
    operation
    direction
    providerId
    provider {
        ...RegularTransactionProvider
        __typename
    }
    user {
        ...RegularUserFragment
        __typename
    }
    creator {
        ...RegularUserFragment
        __typename
    }
    status
    statusDescription
    statusExpirationDate
    value
    fee
    createdAt
    props {
        ...RegularTransactionProps
        __typename
    }
    verifiedAt
    verifiedBy {
        ...UserEdgeNode
        __typename
    }
    completedBy {
        ...UserEdgeNode
        __typename
    }
    paymentMethodId
    completedAt
    isSuspicious
    spbBankName
    __typename
    }

    fragment RegularTransactionProvider on TransactionProvider {
    id
    name
    fee
    minFeeAmount
    description
    account {
        ...RegularTransactionProviderAccount
        __typename
    }
    props {
        ...TransactionProviderPropsFragment
        __typename
    }
    limits {
        ...ProviderLimits
        __typename
    }
    paymentMethods {
        ...TransactionPaymentMethod
        __typename
    }
    __typename
    }

    fragment RegularTransactionProviderAccount on TransactionProviderAccount {
    id
    value
    userId
    __typename
    }

    fragment TransactionProviderPropsFragment on TransactionProviderPropsFragment {
    requiredUserData {
        ...TransactionProviderRequiredUserData
        __typename
    }
    tooltip
    __typename
    }

    fragment TransactionProviderRequiredUserData on TransactionProviderRequiredUserData {
    email
    phoneNumber
    __typename
    }

    fragment ProviderLimits on ProviderLimits {
    incoming {
        ...ProviderLimitRange
        __typename
    }
    outgoing {
        ...ProviderLimitRange
        __typename
    }
    __typename
    }

    fragment ProviderLimitRange on ProviderLimitRange {
    min
    max
    __typename
    }

    fragment TransactionPaymentMethod on TransactionPaymentMethod {
    id
    name
    fee
    providerId
    account {
        ...RegularTransactionProviderAccount
        __typename
    }
    props {
        ...TransactionProviderPropsFragment
        __typename
    }
    limits {
        ...ProviderLimits
        __typename
    }
    __typename
    }

    fragment RegularTransactionProps on TransactionPropsFragment {
    creatorId
    dealId
    paidFromPendingIncome
    paymentURL
    successURL
    fee
    paymentAccount {
        id
        value
        __typename
    }
    paymentGateway
    alreadySpent
    exchangeRate
    amountAfterConversionRub
    amountAfterConversionUsdt
    userData {
        account
        email
        ipAddress
        phoneNumber
        __typename
    }
    __typename
    }

    fragment ChatMessageButton on ChatMessageButton {
    type
    url
    text
    __typename
    }"""
updateItemQuery = """
mutation publishItem($input: PublishItemInput!, $showForbiddenImage: Boolean) {
  publishItem(input: $input) {
    ...RegularItem
    __typename
  }
}

fragment RegularItem on Item {
  ...RegularMyItem
  ...RegularForeignItem
  __typename
}

fragment RegularMyItem on MyItem {
  ...ItemFields
  prevPrice
  priority
  sequence
  priorityPrice
  statusExpirationDate
  comment
  viewsCounter
  statusDescription
  editable
  statusPayment {
    ...StatusPaymentTransaction
    __typename
  }
  moderator {
    id
    username
    __typename
  }
  approvalDate
  deletedAt
  createdAt
  updatedAt
  mayBePublished
  prevFeeMultiplier
  sellerNotifiedAboutFeeChange
  __typename
}

fragment ItemFields on Item {
  id
  slug
  name
  description
  rawPrice
  price
  attributes
  status
  priorityPosition
  sellerType
  feeMultiplier
  user {
    ...ItemUser
    __typename
  }
  buyer {
    ...ItemUser
    __typename
  }
  attachments(showForbiddenImage: $showForbiddenImage) {
    ...PartialFile
    __typename
  }
  isAttachmentsForbidden
  category {
    ...RegularGameCategory
    __typename
  }
  game {
    ...RegularGameProfile
    __typename
  }
  comment
  dataFields {
    ...GameCategoryDataFieldWithValue
    __typename
  }
  obtainingType {
    ...GameCategoryObtainingType
    __typename
  }
  __typename
}

fragment ItemUser on UserFragment {
  ...UserEdgeNode
  __typename
}

fragment UserEdgeNode on UserFragment {
  ...RegularUserFragment
  __typename
}

fragment RegularUserFragment on UserFragment {
  id
  username
  role
  avatarURL
  isOnline
  isBlocked
  rating
  testimonialCounter
  createdAt
  supportChatId
  systemChatId
  __typename
}

fragment PartialFile on File {
  id
  url
  __typename
}

fragment RegularGameCategory on GameCategory {
  id
  slug
  name
  categoryId
  gameId
  obtaining
  options {
    ...RegularGameCategoryOption
    __typename
  }
  props {
    ...GameCategoryProps
    __typename
  }
  noCommentFromBuyer
  instructionForBuyer
  instructionForSeller
  useCustomObtaining
  autoConfirmPeriod
  autoModerationMode
  agreements {
    ...RegularGameCategoryAgreement
    __typename
  }
  feeMultiplier
  __typename
}

fragment RegularGameCategoryOption on GameCategoryOption {
  id
  group
  label
  type
  field
  value
  valueRangeLimit {
    min
    max
    __typename
  }
  __typename
}

fragment GameCategoryProps on GameCategoryPropsObjectType {
  minTestimonials
  minTestimonialsForSeller
  __typename
}

fragment RegularGameCategoryAgreement on GameCategoryAgreement {
  description
  gameCategoryId
  gameCategoryObtainingTypeId
  iconType
  id
  sequence
  __typename
}

fragment RegularGameProfile on GameProfile {
  id
  name
  type
  slug
  logo {
    ...PartialFile
    __typename
  }
  __typename
}

fragment GameCategoryDataFieldWithValue on GameCategoryDataFieldWithValue {
  id
  label
  type
  inputType
  copyable
  hidden
  required
  value
  __typename
}

fragment GameCategoryObtainingType on GameCategoryObtainingType {
  id
  name
  description
  gameCategoryId
  noCommentFromBuyer
  instructionForBuyer
  instructionForSeller
  sequence
  feeMultiplier
  agreements {
    ...MinimalGameCategoryAgreement
    __typename
  }
  props {
    minTestimonialsForSeller
    __typename
  }
  __typename
}

fragment MinimalGameCategoryAgreement on GameCategoryAgreement {
  description
  iconType
  id
  sequence
  __typename
}

fragment StatusPaymentTransaction on Transaction {
  id
  operation
  direction
  providerId
  status
  statusDescription
  statusExpirationDate
  value
  props {
    paymentURL
    __typename
  }
  __typename
}

fragment RegularForeignItem on ForeignItem {
  ...ItemFields
  __typename
}
"""