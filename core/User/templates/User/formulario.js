// JS del formulario de usuario
// --- GraphQL Queries & Mutations ---
const TYPE_DOCUMENTS_QUERY = `query { allTypeDocuments { nameTypeDocument } }`;
const COUNTRIES_QUERY = `query { allCountries { countryName countryCode } }`;
const USERS_QUERY = `query { allUsers { userId username email name lastName isMilitar isTemporal timeCreated userdocumentTb { document typeDocument { nameTypeDocument } placeExpedition dateExpedition } contact { phone celPhone address city countryId { countryName countryCode } emergencyName emergencyPhone } } }`;
const USER_BY_ID_QUERY = id => `query { userById(id: ${id}) { userId username password email name lastName isMilitar isTemporal timeCreated userdocumentTb { document typeDocument { nameTypeDocument } placeExpedition dateExpedition } contact { phone celPhone address city countryId { countryName countryCode } emergencyName emergencyPhone } } }`;
const CREATE_USER_MUTATION = `mutation CreateUser($input: UserAppInput!) { createUser(input: $input) { success message user { userId } } }`;
const UPDATE_USER_MUTATION = `mutation UpdateUser($id: ID!, $user: UpdateUserFields, $document: UpdateDocumentFields, $contact: UpdateContactFields) { updateUser(id: $id, user: $user, document: $document, contact: $contact) { success message user { userId } } }`;
const DELETE_USER_MUTATION = `mutation DeleteUser($id: ID!) { deleteUser(id: $id) { success message } }`;

// --- UI State ---
let users = [];
let filteredUsers = [];
let currentPage = 1;
const pageSize = 10;
let visibleColumns = [
    'userId', 'username', 'email', 'name', 'lastName', 'isMilitar', 'isTemporal',
    'document', 'typeDocument', 'placeExpedition', 'dateExpedition',
    'phone', 'celPhone', 'address', 'city', 'countryName', 'countryCode',
    'emergencyName', 'emergencyPhone', 'timeCreated', 'actions'
];
const allColumns = [
    { key: 'userId', label: 'ID' },
    { key: 'username', label: 'Username' },
    { key: 'email', label: 'Email' },
    { key: 'name', label: 'First Name' },
    { key: 'lastName', label: 'Last Name' },
    { key: 'isMilitar', label: 'Military' },
    { key: 'isTemporal', label: 'Temporal' },
    { key: 'document', label: 'Document' },
    { key: 'typeDocument', label: 'Doc Type' },
    { key: 'placeExpedition', label: 'Place Exp.' },
    { key: 'dateExpedition', label: 'Date Exp.' },
    { key: 'phone', label: 'Phone' },
    { key: 'celPhone', label: 'Cell Phone' },
    { key: 'address', label: 'Address' },
    { key: 'city', label: 'City' },
    { key: 'countryName', label: 'Country' },
    { key: 'countryCode', label: 'Country Code' },
    { key: 'emergencyName', label: 'Emergency Name' },
    { key: 'emergencyPhone', label: 'Emergency Phone' },
    { key: 'timeCreated', label: 'Created At' },
    { key: 'actions', label: 'Actions' }
];

// ... (resto del JS igual que en el HTML, sin cambios de lógica, solo movido aquí) 