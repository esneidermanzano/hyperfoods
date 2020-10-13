// Added views
import Users from "views/Users.js"
import CreateUser from "views/CreateUser.js"

// Template views
import Dashboard from "views/Dashboard.js";
import Icons from "views/Icons.js";
import Map from "views/Map.js";
import Notifications from "views/Notifications.js";
import TableList from "views/TableList.js";
import Typography from "views/Typography.js";
import UserProfile from "views/UserProfile.js";
import CreateTenant from "views/CreateTenat.js"


var routes = [
  // Added views
  {
    path: "/users",
    name: "List Users",
    icon: "tim-icons icon-bullet-list-67",
    component: Users,
    layout: "/admin"
  },
  {
    path: "/create-user",
    name: "Create User",
    icon: "tim-icons icon-single-copy-04",
    component: CreateUser,
    layout: "/admin"
  },
  {
    path: "/create-tenant",
    name: "Crear Tenant",
    icon: "tim-icons icon-chart-pie-36",
    component: CreateTenant,
    layout: "/admin"
  },
  // Template views
  {
    path: "/dashboard",
    name: "Dashboard",
    icon: "tim-icons icon-chart-pie-36",
    component: Dashboard,
    layout: "/admin"
  },
  {
    path: "/icons",
    name: "Icons",    
    icon: "tim-icons icon-atom",
    component: Icons,
    layout: "/admin"
  },
  {
    path: "/map",
    name: "Map",    
    icon: "tim-icons icon-pin",
    component: Map,
    layout: "/admin"
  },
  {
    path: "/notifications",
    name: "Notifications",    
    icon: "tim-icons icon-bell-55",
    component: Notifications,
    layout: "/admin"
  },
  {
    path: "/user-profile",
    name: "User Profile",
    icon: "tim-icons icon-single-02",
    component: UserProfile,
    layout: "/admin"
  },
  {
    path: "/tables",
    name: "Table List",    
    icon: "tim-icons icon-puzzle-10",
    component: TableList,
    layout: "/admin"
  },
  {
    path: "/typography",
    name: "Typography",    
    icon: "tim-icons icon-align-center",
    component: Typography,
    layout: "/admin"
  },  
];
export default routes;
