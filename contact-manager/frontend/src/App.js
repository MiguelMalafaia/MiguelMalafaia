import React, { useState, useEffect } from "react";

function App() {
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Novos estados para o formulário
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");

  // Buscar contactos
  useEffect(() => {
    fetch("http://127.0.0.1:5000/contacts")
      .then((res) => res.json())
      .then((data) => {
        setContacts(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  // Função para enviar novo contacto
  const handleAddContact = (e) => {
    e.preventDefault(); // evita refresh da página
    fetch("http://127.0.0.1:5000/contacts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, phone }),
    })
      .then((res) => res.json())
      .then((data) => {
        setContacts([...contacts, { name, email, phone, id: data.id }]); // atualizar lista
        setName(""); // limpar campos
        setEmail("");
        setPhone("");
      })
      .catch((err) => console.error(err));
  };

  if (loading) return <p>Carregando contactos...</p>;
  if (error) return <p>Erro: {error}</p>;

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Contact Manager</h1>

      {/* Formulário */}
      <form onSubmit={handleAddContact} style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Nome"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Telefone"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
        />
        <button type="submit">Adicionar Contacto</button>
      </form>

      {/* Lista de contactos */}
      {contacts.length === 0 ? (
        <p>Nenhum contacto encontrado.</p>
      ) : (
        <ul>
          {contacts.map((contact) => (
            <li key={contact.id}>
              <strong>{contact.name}</strong> - {contact.email} - {contact.phone}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
