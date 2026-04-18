import { ref } from "vue";

const toasts = ref([]);

let toastId = 0;

export function useToast() {
  const push = ({ title, message, tone = "info", timeout = 2800 }) => {
    const id = ++toastId;
    toasts.value.push({ id, title, message, tone });

    window.setTimeout(() => {
      dismiss(id);
    }, timeout);
  };

  const success = (title, message) => push({ title, message, tone: "success" });
  const error = (title, message) => push({ title, message, tone: "error", timeout: 4200 });
  const info = (title, message) => push({ title, message, tone: "info" });

  return {
    toasts,
    push,
    success,
    error,
    info,
    dismiss,
  };
}

function dismiss(id) {
  toasts.value = toasts.value.filter((toast) => toast.id !== id);
}
