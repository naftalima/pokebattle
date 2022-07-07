export function getUserName(email) {
  if (email && email.includes('@')) return email.split('@')[0];
  return email;
}
