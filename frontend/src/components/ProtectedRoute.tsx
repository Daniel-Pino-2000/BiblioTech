import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

/** Route guard: redirects to /login if logged out, or to / if `adminOnly`
 * is set and the user isn't an admin. Wrap any element that needs one. */
export function ProtectedRoute({
  children,
  adminOnly = false,
}: {
  children: ReactNode;
  adminOnly?: boolean;
}) {
  const { user, loading } = useAuth();

  if (loading) return <div className="page-status">Loading...</div>;
  if (!user) return <Navigate to="/login" replace />;
  if (adminOnly && !user.is_admin) return <Navigate to="/" replace />;

  return <>{children}</>;
}
