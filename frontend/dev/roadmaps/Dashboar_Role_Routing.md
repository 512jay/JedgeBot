# 📊 JedgeBot Dashboard Role Routing Roadmap

## 🎯 Goal: Split + RoleRedirector + Shared Layout Strategy

Create a scalable, role-aware dashboard system using:
- ✅ Role-specific dashboards (`/dashboard/manager`, `/dashboard/client`, etc.)
- ✅ Shared layout (`Sidebar`, greeting, etc.)
- ✅ Automatic redirection from `/dashboard` based on the user's role

---

## 🗺️ Step-by-Step Roadmap

### ✅ Step 1: `RoleRedirector.jsx`
Redirect users based on their role:

```jsx
// /frontend/src/pages/RoleRedirector.jsx
import { useAuth } from "@/context/AuthContext";
import { Navigate } from "react-router-dom";

const RoleRedirector = () => {
  const { user } = useAuth();

  if (!user) return <Navigate to="/login" />;

  switch (user.role) {
    case "free":
    case "client":
      return <Navigate to={`/dashboard/${user.role}`} />;
    case "manager":
      return <Navigate to="/dashboard/manager" />;
    case "enterprise":
      return <Navigate to="/dashboard/enterprise" />;
    default:
      return <Navigate to="/unauthorized" />;
  }
};

export default RoleRedirector;
```

---

### ✅ Step 2: Update `AppRoutes.jsx`

```jsx
import RoleRedirector from "@/pages/RoleRedirector";

<Route element={<PrivateRoute />}>
  <Route path="/dashboard" element={<RoleRedirector />} />
  <Route path="/dashboard/free" element={<FreeDashboard />} />
  <Route path="/dashboard/client" element={<ClientDashboard />} />
  <Route path="/dashboard/manager" element={<ManagerDashboard />} />
  <Route path="/dashboard/enterprise" element={<EnterpriseDashboard />} />
</Route>
```

---

### ✅ Step 3: Shared Layout Component

```jsx
// /components/layout/DashboardLayout.jsx
import Sidebar from "@/components/layout/Sidebar";
import { useAuth } from "@/context/AuthContext";

const DashboardLayout = ({ children }) => {
  const { user } = useAuth();

  return (
    <div style={{ display: "flex", height: "100vh", width: "100vw" }}>
      <Sidebar />
      <div style={{ flex: 1, backgroundColor: "#6495ED", padding: "2rem", overflowY: "auto" }}>
        <h1 style={{ fontSize: "2.5rem", fontWeight: "600", marginBottom: "2rem", color: "white" }}>
          Welcome {user?.username || "Trader"}
        </h1>
        {children}
      </div>
    </div>
  );
};

export default DashboardLayout;
```

---

### ✅ Step 4: Create Role-Specific Dashboards

```jsx
// /pages/dashboard/ClientDashboard.jsx
import DashboardLayout from "@/components/layout/DashboardLayout";
import DashboardCards from "@/components/DashboardCards";

const ClientDashboard = () => {
  return (
    <DashboardLayout>
      <DashboardCards />
      {/* Add client-specific features here */}
    </DashboardLayout>
  );
};

export default ClientDashboard;
```

Repeat for: `FreeDashboard.jsx`, `ManagerDashboard.jsx`, `EnterpriseDashboard.jsx`

---

### ✅ Step 5: Sidebar Role-Based Links

```jsx
const { user } = useAuth();

{user?.role === 'manager' && (
  <MDBListGroupItem>
    <Link to="/create-client">Create Client</Link>
  </MDBListGroupItem>
)}

{user?.role === 'enterprise' && (
  <>
    <MDBListGroupItem>
      <Link to="/create-manager">Create Manager</Link>
    </MDBListGroupItem>
    <MDBListGroupItem>
      <Link to="/create-client">Create Client</Link>
    </MDBListGroupItem>
    <MDBListGroupItem>
      <Link to="/create-account">Create Account</Link>
    </MDBListGroupItem>
  </>
)}
```

---

### ✅ Step 6: (Optional) Remove Old `Dashboard.jsx`
Once new dashboards are functional, `Dashboard.jsx` can be removed or converted to a fallback.

---

## 🧠 Summary

| Feature | Status |
|--------|--------|
| One shared layout | ✅ `DashboardLayout.jsx` |
| Separate dashboards | ✅ Role-specific dashboard components |
| Smart redirect | ✅ `RoleRedirector.jsx` |
| Secure routing | ✅ `PrivateRoute` per role |
| Role-aware sidebar | ✅ Dynamic links in `Sidebar.jsx` |

Use this roadmap to keep your dashboard system clean, scalable, and user-friendly as JedgeBot grows. 🚀

