<template>
  <div class="Container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Cadastro de pessoas</h1>
        <hr>
        <br>
        <alert :message="message" v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm"
                v-b-modal.pessoa-modal>Adicionar Registro</button>
        <br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Nome</th>
              <th scope="col">Idade</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(pessoa, index) in pessoas" :key="index">
              <td>{{pessoa.nome}}</td>
              <td>{{pessoa.idade}}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm"
                          v-b-modal.pessoa-update-modal
                          @click="editPessoa(pessoa)">Atualizar</button>
                  <button type="button" class="btn btn-danger btn-sm"
                          @click="onDeletePessoa(pessoa)">Deletar</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addPessoasModal" id="pessoa-modal" title="Inclua um novo registro" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-nome-group" label="Nome:" label-for="form-nome-input">
          <b-form-input id="form-nome-input"
                        type="text"
                        v-model="addPessoasForm.nome"
                        required
                        placeholder="Digite o nome"></b-form-input>
        </b-form-group>
        <b-form-group id="form-datanascimento-group"
                      label="Data de Nascimento:"
                      label-for="form-datanascimento-input">
          <b-form-input id="form-datanascimento-input"
                        type="text"
                        v-model="addPessoasForm.nascimento"
                        required
                        placeholder="Data de Nascimento: DD/MM/AAAA"></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Confirmar</b-button>
        <b-button type="reset" variant="danger">Limpar</b-button>
      </b-form>
    </b-modal>
    <b-modal ref="editPessoaModal"
        id="pessoa-update-modal"
        title="Update"
        hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-nome-edit-group"
                    label="Nome:"
                    label-for="form-nome-edit-input">
          <b-form-input id="form-nome-edit-input"
                        type="text"
                        v-model="editForm.nome"
                        required
                        placeholder="Digite o Nome:">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-nascimento-edit-group"
                      label="Data de nascimento:"
                      label-for="form-nascimento-edit-input">
          <b-form-input id="form-nascimento-edit-input"
                          type="text"
                          v-model="editForm.nascimento"
                          required
                          placeholder="Data de Nascimento: DD/MM/AAAA">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Atualizar</b-button>
          <b-button type="reset" variant="danger">Cancelar</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      pessoas: [],
      addPessoasForm: {
        nome: '',
        nascimento: '',
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        nome: '',
        nascimento: '',
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getPessoas() {
      const path = 'http://localhost:5000/pessoas';
      axios.get(path)
        .then((res) => {
          this.pessoas = res.data.pessoas;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addPessoas(payLoad) {
      const path = 'http://localhost:5000/pessoas';
      axios.post(path, payLoad)
        .then(() => {
          this.getPessoas();
          this.message = 'Pessoa cadastrada com sucesso!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.log(error);
          this.getPessoas();
        });
    },
    updatePessoa(payLoad, pessoaID) {
      const path = `http://localhost:5000/pessoas/${pessoaID}`;
      axios.put(path, payLoad)
        .then(() => {
          this.getPessoas();
          this.message = 'Dados de pessoa atualizados!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getPessoas();
        });
    },
    removePessoa(pessoaID) {
      const path = `http://localhost:5000/pessoas/${pessoaID}`;
      axios.delete(path)
        .then(() => {
          this.getPessoas();
          this.message = 'Pessoa Excluída!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getPessoas();
        });
    },
    editPessoa(pessoa) {
      this.editForm = pessoa;
    },
    initForm() {
      this.addPessoasForm.nome = '';
      this.addPessoasForm.nascimento = '';
      this.editForm.id = '';
      this.editForm.nome = '';
      this.editForm.nascimento = '';
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editPessoaModal.hide();
      const payLoad = {
        nome: this.editForm.nome,
        nascimento: this.editForm.nascimento,
      };
      this.updatePessoa(payLoad, this.editForm.id);
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addPessoasModal.hide();
      const payLoad = {
        nome: this.addPessoasForm.nome,
        nascimento: this.addPessoasForm.nascimento,
      };
      this.addPessoas(payLoad);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addPessoasModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.editPessoaModal.hide();
      this.initForm();
      this.getPessoas();
    },
    onDeletePessoa(pessoa) {
      this.removePessoa(pessoa.id);
    },
  },
  created() {
    this.getPessoas();
  },
};
</script>
