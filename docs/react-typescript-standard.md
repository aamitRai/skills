# TypeScript React Coding Standards

## 1. Use Strict TypeScript

Always enable strict mode in `tsconfig.json`.

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

### Why?

- Prevents runtime bugs
- Improves IntelliSense and autocomplete
- Makes refactoring safer
- Enforces better type safety

---

## 2. Create Typed Interfaces

Prefer `interface` for component props.

```tsx
interface ButtonProps {
  title: string;
  onClick: () => void;
  disabled?: boolean;
}

const Button = ({ title, onClick, disabled }: ButtonProps) => {
  return (
    <button onClick={onClick} disabled={disabled}>
      {title}
    </button>
  );
};
```

### Best Practices

- Use `interface` for component props.
- Keep interfaces small and reusable.
- Extend interfaces when needed instead of duplicating types.

---

## 3. Never Use `any`

Avoid using `any` as it removes TypeScript's type safety.

### ❌ Bad

```ts
const data: any = response;
```

### ✅ Good

```ts
interface User {
  id: number;
  name: string;
}

const data: User = response;
```

### Prefer Using

- `unknown`
- Generics (`<T>`)
- Interfaces
- Type aliases

instead of `any`.

---

## 4. Separate the API Layer

Do not call APIs directly inside React components.

### ❌ Bad

```tsx
useEffect(() => {
  axios.get("/users");
}, []);
```

### ✅ Good

```ts
// services/userService.ts
export const getUsers = () => api.get("/users");
```

```tsx
const { data } = useQuery({
  queryKey: ["users"],
  queryFn: getUsers,
});
```

### Benefits

- Better separation of concerns
- Easier testing
- Reusable API functions
- Cleaner components

---

## 5. Prefer Functional Components and Hooks

Avoid class components. Use functional components with React Hooks.

```tsx
const Profile = () => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // Fetch data
  }, []);

  return <div />;
};
```

### Benefits

- Simpler code
- Better readability
- Easier state management
- Modern React standard

---

## 6. Use Consistent Naming Conventions

### Components (PascalCase)

```text
UserCard.tsx
LoginForm.tsx
InterviewCard.tsx
```

### Hooks (`use` Prefix)

```text
useAuth.ts
useInterview.ts
```

### Utilities (camelCase)

```text
formatDate.ts
validateEmail.ts
```

### Interfaces (PascalCase)

```ts
interface User {}

interface Interview {}

interface ApiResponse<T> {}
```

### Constants (UPPER_SNAKE_CASE)

```ts
export const API_TIMEOUT = 30000;
```

---

## Summary

- ✅ Enable strict TypeScript mode.
- ✅ Define interfaces for props and data models.
- ✅ Avoid `any`; use proper types instead.
- ✅ Keep API logic outside components.
- ✅ Prefer functional components with Hooks.
- ✅ Follow consistent naming conventions across the project.