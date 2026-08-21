import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

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
